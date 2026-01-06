"""
Creates and fetches all data necessary for the current User
"""
import json

from Infrastructure.Database.Database import Database
from Modules.Enums.Sport import Sport
from Modules.League.League import League
from Modules.League.Team import Team
from Modules.SleeperApi.SleeperApi import SleeperApi
from Modules.User.User import User
from Modules.User.UserFactory.IUserFactory import IUserFactory
from Modules.Util.ComplexNamespace import ComplexNamespace


class UserFactory(IUserFactory):
    def __init__(self, api: SleeperApi, db: Database):
        self.api = api
        self.db = db

    def get_user(self, username: str) -> User:
        return self._get_user(username)

    # region Private Method(s)
    def _get_user(self, username: str) -> User:
        # TODO: check if user already exists in DB and pull that

        # if not, get from Sleeper Api
        endpoint = f"user/{username}"
        response = self.api.get(endpoint)
        user_obj = json.loads(response, object_hook=lambda d: ComplexNamespace(**d))
        user = User(user_obj.username, user_obj.user_id, user_obj.display_name, user_obj.avatar,
                    self._get_leagues(user_obj.user_id))

        # TODO: add user to database or update if username was changed

        return user

    def _get_leagues(self, user_id: int) -> list[League]:

        leagues = []
        for sport in Sport:
            season_year = self._get_sport_season_year(sport)

            # TODO: check if user already exists in DB

            # if not, get from Sleeper Api for each
            endpoint = f"user/{user_id}/leagues/{sport.name.lower()}/{season_year}"
            response = self.api.get(endpoint)
            leagues_obj = json.loads(response, object_hook=lambda d: ComplexNamespace(**d))

            for l in leagues_obj:
                teams = self._get_teams_in_league(l.league_id)
                leagues.append(League(l.league_id, Sport.convert(l.sport), l.season, l.name, teams))

        return leagues

    def _get_sport_season_year(self, sport: Sport) -> str:
        endpoint = f"state/{sport.name.lower()}"
        response = self.api.get(endpoint)
        state = json.loads(response, object_hook=lambda d: ComplexNamespace(**d))

        return state.season

    def _get_teams_in_league(self, league_id: str) -> list[Team]:
        teams = []

        endpoint = f"/league/{league_id}/users"
        response = self.api.get(endpoint)
        teams_obj = json.loads(response, object_hook=lambda item: ComplexNamespace(**item))

        for team in teams_obj:
            nickname = team.metadata.team_name if hasattr(team.metadata, "team_name") else team.display_name
            teams.append(Team(team.user_id, team.display_name, team.avatar, nickname, team.is_owner))

        return teams
    # endregion
