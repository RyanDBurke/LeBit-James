from Modules.Enums.Sport import Sport
from Modules.League.Team import Team


class League:
    def __init__(self, league_id: str, sport: Sport, season_year: str, name: str, teams: list[Team] = None):
        self.league_id = league_id
        self.sport = Sport.convert(sport) if isinstance(sport, str) else sport
        self.season_year = season_year
        self.name = name
        self.teams = teams

    def __repr__(self):
        return f"League({self.name} | {self.season_year} | {self.sport})"
