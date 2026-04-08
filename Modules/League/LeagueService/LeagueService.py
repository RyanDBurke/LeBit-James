"""
League service implementation
"""
import json
from datetime import datetime

from Infrastructure.Database.Database import Database
from Modules.Enums.Sport import Sport
from Modules.League.League import League
from Modules.League.LeagueService.ILeagueService import ILeagueService
from Modules.League.Team import Team
from Modules.SleeperApi.SleeperApi import SleeperApi
from Modules.Util.ComplexNamespace import ComplexNamespace


class LeagueService(ILeagueService):
    def __init__(self, api: SleeperApi, db: Database):
        self.api = api
        self.db = db

    def refresh_leagues(self, user_id: str) -> list[League]:
        # clear existing leagues for this user before re-inserting
        delete_sql = """DELETE FROM "League" WHERE user_id = %s"""
        self.db.execute(delete_sql, (user_id.lower(),))

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
