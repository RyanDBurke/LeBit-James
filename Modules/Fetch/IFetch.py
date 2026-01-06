"""
Interface for fetching data from external APIs
"""

from abc import ABC, abstractmethod

class IFetch(ABC):
    @abstractmethod
    def fetch(self, url: str) -> str | None:
        pass