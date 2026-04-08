from PyQt6.QtCore import QObject, pyqtSlot


class About(QObject):
    def __init__(self, navigator, engine):
        super().__init__()
        self._navigator = navigator
        engine.rootContext().setContextProperty("aboutHandler", self)

    @pyqtSlot()
    def goHome(self):
        self._navigator.navigate("../Home/home.qml")
