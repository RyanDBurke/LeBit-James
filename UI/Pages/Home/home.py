from PyQt6.QtCore import QObject, pyqtSlot


class Home(QObject):
    def __init__(self, navigator, login_handler, leagues_handler, engine):
        super().__init__()
        self._navigator = navigator
        self._login_handler = login_handler
        self._leagues_handler = leagues_handler
        engine.rootContext().setContextProperty("homeHandler", self)

    @pyqtSlot()
    def goHome(self):
        self._navigator.navigate("../Home/home.qml")

    @pyqtSlot()
    def goAbout(self):
        self._navigator.navigate("../About/about.qml")

    @pyqtSlot(str)
    def goLeagues(self, sport: str = ""):
        if sport:
            self._leagues_handler.setSportFilter(sport)
        self._navigator.navigate("../Leagues/leagues.qml")

    @pyqtSlot()
    def logout(self):
        self._login_handler.logout()
