"""
Creates and fetches all data necessary for the current User
"""
import json
from datetime import datetime

from Infrastructure.Database.Database import Database
from Modules.Enums.Sport import Sport
from Modules.League.League import League
from Modules.League.Team import Team
from Modules.SleeperApi.SleeperApi import SleeperApi
from Modules.User.User import User
from Modules.User.UserService.IUserService import IUserService
from Modules.Util.ComplexNamespace import ComplexNamespace


class UserService(IUserService):
    def __init__(self, api: SleeperApi, db: Database):
        self.api = api
        self.db = db

    def get_user(self, username: str):
        return self._get_user(username)

    # region Private Method(s)
    def _get_user(self, username: str) -> User:
        # check if a user already exists in DB
        user_sql = """SELECT *
                      FROM "Users"
                      WHERE username = %s LIMIT 1"""
        user_result = self.db.execute(user_sql, (username.lower(),), User)

        # if it exists, return it from DB
        if user_result:
            if isinstance(user_result[0], User):
                user: User = user_result[0]
                user.leagues = self._get_leagues(user.user_id)
                return user

        # otherwise, get User from Sleeper Api
        endpoint = f"user/{username}"
        response = self.api.get(endpoint)

        # user doesn't exist, let's gtf outta here
        if not response or response == "null":
            return None

        user_obj = json.loads(response, object_hook=lambda d: ComplexNamespace(**d))
        user = User(user_obj.username, user_obj.user_id, user_obj.display_name, user_obj.avatar,
                    self._get_leagues(user_obj.user_id))

        # Add a user to the db or update their username if it was changed
        user_id_sql = """SELECT *
                         FROM "Users"
                         WHERE user_id = %s LIMIT 1"""
        user_id_result = self.db.execute(user_id_sql, (user.user_id.lower(),), User)

        # update existing row with new username
        if user_id_result:
            user_update_username_sql = """UPDATE "Users"
                                          SET username = %s
                                          WHERE user_id = %s"""
            self.db.execute(user_update_username_sql, (user.username.lower(), user.user_id.lower()))
        else:
            user_upsert_sql = """INSERT INTO "Users" (user_id, username, display_name, avatar_id)
                                 VALUES (%s, %s, %s, %s)"""
            self.db.execute(user_upsert_sql, (user.user_id.lower(), user.username.lower(), user.display_name.lower(),
                                              user.avatar_id.lower()))

        return user

    def _get_leagues(self, user_id: str) -> list[League]:
        # see if user's leagues are already in db
        league_sql = """SELECT league_id, sport, season_year, name
                        FROM "League"
                        WHERE user_id = %s"""
        leagues_result = self.db.execute(league_sql, (user_id.lower(),), League)

        # if so, return leagues
        if leagues_result:
            leagues = []
            for l in leagues_result:
                if isinstance(l, League):
                    league: League = l
                    league.teams = self._get_teams_in_league(league.league_id)
                    leagues.append(league)
            return leagues

        # otherwise, let's get all these user's leagues
        leagues = []
        current_year = datetime.now().year
        for sport in Sport:
            for season_year in range(current_year - 1, current_year - 4, -1):
                endpoint = f"user/{user_id}/leagues/{sport.name.lower()}/{season_year}"
                response = self.api.get(endpoint)
                leagues_obj = json.loads(response, object_hook=lambda d: ComplexNamespace(**d))

                for l in leagues_obj:
                    teams = self._get_teams_in_league(l.league_id)
                    league = League(l.league_id, Sport.convert(l.sport), l.season, l.name, teams)
                    leagues.append(league)

                    # add all their leagues to the db
                    for t in teams:
                        league_upsert_sql = """INSERT INTO "League" (league_id, sport, season_year, name, user_id)
                                               VALUES (%s, %s, %s, %s, %s)"""
                        self.db.execute(league_upsert_sql,
                                        (league.league_id, league.sport.name.lower(), league.season_year, league.name,
                                         t.user_id))
        return leagues

    def _get_teams_in_league(self, league_id: str) -> list[Team]:
        teams = []
        endpoint = f"/league/{league_id}/users"
        response = self.api.get(endpoint)
        teams_obj = json.loads(response, object_hook=lambda item: ComplexNamespace(**item))

        for team in teams_obj:
            nickname = team.metadata.team_name if hasattr(team.metadata, "team_name") else team.display_name
            teams.append(Team(league_id, team.user_id, team.display_name, team.avatar, nickname, team.is_owner))

        return teams
    # endregion
