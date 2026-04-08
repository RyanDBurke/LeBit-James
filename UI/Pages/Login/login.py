from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty

from Infrastructure.Configuration.Container import Container


class Login(QObject):
    usernameSubmitted = pyqtSignal(str)
    loginSuccessChanged = pyqtSignal()
    loadingChanged = pyqtSignal()
    errorMessageChanged = pyqtSignal()
    cachedUsernamesChanged = pyqtSignal(list)
    userLoaded = pyqtSignal(object)

    def __init__(self, engine, navigator):
        super().__init__()
        self._login_success = False
        self._loading = False
        self._error_message = ""
        self._current_username = ""
        self._fetched_user = None
        self._navigator = navigator
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

    def set_fetched_user(self, user):
        self._fetched_user = user

    @pyqtSlot(str)
    def submit(self, username):
        if not username.strip():
            self._error_message = "please enter a username"
            self.errorMessageChanged.emit()
            return
        if self._loading:
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

        if self._fetched_user is not None:
            self.userLoaded.emit(self._fetched_user)
            self._fetched_user = None

        # Add username to cache on successful login
        if self._current_username:
            self.username_cache.add_username(self._current_username)

            # Emit signal to update cached usernames in UI
            self.cachedUsernamesChanged.emit(self._format_cached_usernames())
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
        """Get list of cached usernames with their metadata."""
        return self._format_cached_usernames()

    @pyqtSlot(str)
    def removeCachedUsername(self, username: str):
        """Remove a username from the cache."""
        self.username_cache.remove_username(username)
        # Emit signal with updated list
        self.cachedUsernamesChanged.emit(self._format_cached_usernames())

    @pyqtSlot(str)
    def toggleFavorite(self, username: str):
        """Toggle the favorite status of a cached username."""
        self.username_cache.toggle_favorite(username)

        # Emit signal with updated list
        self.cachedUsernamesChanged.emit(self._format_cached_usernames())

    def _format_cached_usernames(self):
        """Format cached usernames for QML consumption."""
        usernames = self.username_cache.get_cached_usernames()
        
        # Return list of dictionaries with username and is_favorite for QML
        return [{"username": u.get("username"), "is_favorite": u.get("is_favorite", False)} for u in usernames]

    @pyqtSlot()
    def logout(self):
        self._login_success = False
        self._loading = False
        self._error_message = ""
        self.loginSuccessChanged.emit()
        self.loadingChanged.emit()
        self.errorMessageChanged.emit()
        self._navigator.reset()
        # Refresh cached usernames when returning to login
        self.cachedUsernamesChanged.emit(self._format_cached_usernames())