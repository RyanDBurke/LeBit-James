"""
Interface for fetching User data from Sleeper API
"""
from abc import ABC, abstractmethod
from Modules.User.User import User


class IUserService(ABC):
    @abstractmethod
    def get_user(self, username: str) -> User:
        pass