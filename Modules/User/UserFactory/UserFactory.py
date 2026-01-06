"""
Creates and fetches all data necessary for a single User
"""
import json
from types import SimpleNamespace

from Modules.Enums.Sport import Sport
from Modules.League.League import League
from Modules.SleeperApi.SleeperApi import SleeperApi
from Modules.User.User import User
from Modules.User.UserFactory.IUserFactory import IUserFactory


class UserFactory(IUserFactory):
    def __init__(self, api: SleeperApi):
        self.api = api

    def get_user(self, username: str) -> User:
        return self._get_user(username)

    # region Private Method(s)
    def _get_user(self, username: str) -> User:
        # check if user already exists in DB and pull that

        # if not, get from Sleeper Api
        endpoint = f"user/{username}"
        response = self.api.get(endpoint)
        user_obj = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
        user = User(user_obj.username, user_obj.user_id, user_obj.display_name, user_obj.avatar, self._get_leagues(user_obj.user_id))

        # add user to database or update if username was changed

        return user

    def _get_leagues(self, user_id: int) -> list[League]:

        leagues = []
        for sport in Sport:
            season_year = self._get_sport_season_year(sport)

            # check if user already exists in DB

            # if not, get from Sleeper Api for each
            endpoint = f"user/{user_id}/leagues/{sport.name.lower()}/{season_year}"
            response = self.api.get(endpoint)
            leagues_obj = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))

            for l in leagues_obj:
                leagues.append(League(l.league_id, Sport.convert(l.sport), l.season, l.name))

        return leagues

    def _get_sport_season_year(self, sport: Sport) -> str:
        endpoint = f"state/{sport.name.lower()}"
        response = self.api.get(endpoint)
        state = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))

        return state.season
    # endregion