from abc import ABC, abstractmethod
from typing import List


class IUsernameCache(ABC):
    """Interface for managing cached usernames."""

    @abstractmethod
    def get_cached_usernames(self) -> List[str]:
        """
        Retrieve all cached usernames.

        Returns:
            List of cached usernames in order of storage.
        """
        pass

    @abstractmethod
    def add_username(self, username: str) -> None:
        """
        Add a username to the cache if it doesn't already exist.

        Args:
            username: The username to add.
        """
        pass

    @abstractmethod
    def remove_username(self, username: str) -> None:
        """
        Remove a specific username from the cache.

        Args:
            username: The username to remove.
        """
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Clear all cached usernames."""
        pass
