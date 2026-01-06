from Modules.Enums.Sport import Sport

class League:
    def __init__(self, league_id: int, sport: Sport, season_year: str, name: str):
        self.league_id = league_id
        self.sport = sport
        self.season_year = season_year
        self.name = name