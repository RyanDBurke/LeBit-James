from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty


class Navigator(QObject):
    currentPageChanged = pyqtSignal()

    def __init__(self, engine):
        super().__init__()
        self._current_page = "../Home/home.qml"
        self.engine = engine
        self.engine.rootContext().setContextProperty("navigator", self)

    @pyqtProperty(str, notify=currentPageChanged)
    def currentPage(self):
        return self._current_page

    def navigate(self, page: str):
        self._current_page = ""
        self.currentPageChanged.emit()
        self._current_page = page
        self.currentPageChanged.emit()

    def reset(self):
        self._current_page = "../Home/home.qml"
        self.currentPageChanged.emit()
