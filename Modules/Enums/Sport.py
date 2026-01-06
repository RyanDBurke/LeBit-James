from enum import Enum

class Sport(Enum):
    NBA = 1
    NFL = 2

    @staticmethod
    def convert(sport: str):
        match sport.lower():
            case "nba":
                return Sport.NBA
            case "nfl":
                return Sport.NFL
            case _:
                return Sport.NBA
