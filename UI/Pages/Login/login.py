from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty

from Infrastructure.Configuration.Container import Container


class Login(QObject):
    usernameSubmitted = pyqtSignal(str)
    loginSuccessChanged = pyqtSignal()
    loadingChanged = pyqtSignal()
    errorMessageChanged = pyqtSignal()
    currentPageChanged = pyqtSignal()
    cachedUsernamesChanged = pyqtSignal(list)

    def __init__(self, engine):
        super().__init__()
        self._login_success = False
        self._loading = False
        self._error_message = ""
        self._current_page = "../Home/home.qml"
        self._current_username = ""
        self.engine = engine
        # Resolve dependency from container
        self.username_cache = Container.username_cache()
        self.engine.rootContext().setContextProperty("loginHandler", self)

    @pyqtProperty(bool, notify=loginSuccessChanged)
    def loginSuccess(self):
        return self._login_success

    @pyqtProperty(bool, notify=loadingChanged)
    def loading(self):
        return self._loading

    @pyqtProperty(str, notify=errorMessageChanged)
    def errorMessage(self):
        return self._error_message

    @pyqtProperty(str, notify=currentPageChanged)
    def currentPage(self):
        return self._current_page

    @pyqtSlot(str)
    def submit(self, username):
        if not username.strip():
            self._error_message = "please enter a username"
            self.errorMessageChanged.emit()
            return
        self._current_username = username.strip()
        self._error_message = ""
        self.errorMessageChanged.emit()
        self._loading = True
        self.loadingChanged.emit()
        self.usernameSubmitted.emit(username)

    @pyqtSlot()
    def onLoginSuccess(self):
        self._loading = False
        self.loadingChanged.emit()
        # Add username to cache on successful login
        if self._current_username:
            self.username_cache.add_username(self._current_username)
            self._current_username = ""
        self._login_success = True
        self.loginSuccessChanged.emit()

    @pyqtSlot()
    def onLoginFailed(self):
        self._loading = False
        self.loadingChanged.emit()
        self._error_message = "user doesn't exist!"
        self.errorMessageChanged.emit()

    @pyqtSlot(result=list)
    def getCachedUsernames(self):
        """Get list of cached usernames."""
        return self.username_cache.get_cached_usernames()

    @pyqtSlot(str)
    def removeCachedUsername(self, username: str):
        """Remove a username from the cache."""
        self.username_cache.remove_username(username)
        # Emit signal with updated list
        self.cachedUsernamesChanged.emit(self.username_cache.get_cached_usernames())

    @pyqtSlot()
    def logout(self):
        self._login_success = False
        self._loading = False
        self._error_message = ""
        self._current_page = "../Home/home.qml"
        self.loginSuccessChanged.emit()
        self.loadingChanged.emit()
        self.errorMessageChanged.emit()
        self.currentPageChanged.emit()

    @pyqtSlot()
    def goHome(self):
        self._current_page = ""
        self.currentPageChanged.emit()
        self._current_page = "../Home/home.qml"
        self.currentPageChanged.emit()

    @pyqtSlot()
    def goAbout(self):
        self._current_page = ""
        self.currentPageChanged.emit()
        self._current_page = "../About/about.qml"
        self.currentPageChanged.emit()
