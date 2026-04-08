import logging
import threading
import time

from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QMetaObject, QTimer, Qt

from Modules.Enums.Sport import Sport
from Modules.League.LeagueService.ILeagueService import ILeagueService

logger = logging.getLogger(__name__)


class Leagues(QObject):
    _SPORT_NAMES = {
        Sport.NBA: "basketball",
        Sport.NFL: "football",
    }

    leaguesChanged = pyqtSignal()
    userReprChanged = pyqtSignal()
    sportNameChanged = pyqtSignal()
    newLeagueIdsChanged = pyqtSignal()
    refreshFinished = pyqtSignal()
    refreshingChanged = pyqtSignal()
    refreshCooldownChanged = pyqtSignal()

    def __init__(self, navigator, login_handler, engine, league_service: ILeagueService = None):
        super().__init__()
        self._navigator = navigator
        self._login_handler = login_handler
        self._league_service = league_service
        self._user = None
        self._sport_filter = None
        self._leagues = []
        self._new_league_ids = []
        self._refreshing = False
        self._refresh_timestamps = []
        self._refresh_cooldown = False
        self._cooldown_timer = QTimer(self)
        self._cooldown_timer.setSingleShot(True)
        self._cooldown_timer.timeout.connect(self._end_cooldown)
        self.refreshFinished.connect(self._on_refresh_finished)
        engine.rootContext().setContextProperty("leaguesHandler", self)

    @pyqtProperty(str, notify=userReprChanged)
    def userRepr(self):
        return repr(self._user) if self._user is not None else ""

    @pyqtSlot(object)
    def setUser(self, user):
        self._user = user
        self.userReprChanged.emit()
        self._update_leagues()

    @pyqtSlot(str)
    def setSportFilter(self, sport: str):
        self._sport_filter = Sport.convert(sport)
        self.sportNameChanged.emit()
        self._update_leagues()

    @pyqtProperty(str, notify=sportNameChanged)
    def sportName(self):
        if self._sport_filter is None:
            return ""
        return self._SPORT_NAMES.get(self._sport_filter, "")

    def _update_leagues(self):
        if self._user is None or self._user.leagues is None:
            self._leagues = []
        elif self._sport_filter is None:
            self._leagues = [{
                "name": l.name,
                "league_id": l.league_id,
                "season_year": l.season_year
            } for l in self._user.leagues]
        else:
            self._leagues = [
                {
                    "name": l.name,
                    "league_id": l.league_id,
                    "season_year": l.season_year
                }
                for l in self._user.leagues
                if l.sport == self._sport_filter
            ]
        self.leaguesChanged.emit()

    @pyqtProperty(list, notify=leaguesChanged)
    def leagues(self):
        return self._leagues

    @pyqtProperty(list, notify=newLeagueIdsChanged)
    def newLeagueIds(self):
        return self._new_league_ids

    @pyqtProperty(bool, notify=refreshingChanged)
    def refreshing(self):
        return self._refreshing

    @pyqtProperty(bool, notify=refreshCooldownChanged)
    def refreshCooldown(self):
        return self._refresh_cooldown

    @pyqtSlot()
    def refresh(self):
        if self._refresh_cooldown or self._refreshing:
            return
        if not self._league_service or not self._user:
            return

        now = time.monotonic()
        self._refresh_timestamps = [t for t in self._refresh_timestamps if now - t < 60]
        self._refresh_timestamps.append(now)

        if len(self._refresh_timestamps) >= 2:
            self._refresh_cooldown = True
            self.refreshCooldownChanged.emit()
            self._cooldown_timer.start(10000)
            return

        self._refreshing = True
        self.refreshingChanged.emit()

        def _do_refresh():
            try:
                old_ids = {l.league_id for l in self._user.leagues} if self._user.leagues else set()
                refreshed = self._league_service.refresh_leagues(self._user.user_id)
                self._user.leagues = refreshed
                new_ids = {l.league_id for l in refreshed} if refreshed else set()
                self._new_league_ids = list(new_ids - old_ids)
            except Exception:
                logger.exception("League refresh failed")
            QMetaObject.invokeMethod(self, "onRefreshFinished", Qt.ConnectionType.QueuedConnection)

        threading.Thread(target=_do_refresh, daemon=True).start()

    @pyqtSlot()
    def onRefreshFinished(self):
        self.refreshFinished.emit()

    def _on_refresh_finished(self):
        self._refreshing = False
        self.refreshingChanged.emit()
        self._update_leagues()
        self.newLeagueIdsChanged.emit()

    def _end_cooldown(self):
        self._refresh_cooldown = False
        self._refresh_timestamps.clear()
        self.refreshCooldownChanged.emit()

    @pyqtSlot()
    def clearNewLeagueIds(self):
        self._new_league_ids = []
        self.newLeagueIdsChanged.emit()

    @pyqtSlot()
    def goHome(self):
        self._navigator.navigate("../Home/home.qml")

    @pyqtSlot()
    def logout(self):
        self._login_handler.logout()