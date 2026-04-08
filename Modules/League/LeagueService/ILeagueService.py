"""
Interface for League service operations
"""
from abc import ABC, abstractmethod

from Modules.League.League import League


class ILeagueService(ABC):
    @abstractmethod
    def refresh_leagues(self, user_id: str) -> list[League]:
        pass
