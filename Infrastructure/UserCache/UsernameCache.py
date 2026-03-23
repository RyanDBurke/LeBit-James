import json
import logging
from pathlib import Path
from typing import List
from threading import Lock

from Infrastructure.UserCache.IUsernameCache import IUsernameCache


logger = logging.getLogger(__name__)


class UsernameCache(IUsernameCache):
    """Manages cached usernames stored in a local JSON file."""

    MAX_CACHED_USERNAMES = 5

    def __init__(self, cache_dir: str = None):
        """
        Initialize the username cache.

        Args:
            cache_dir: Directory path where cache file will be stored.
                      If None, uses ~/.lebit/ directory.
        """
        if cache_dir is None:
            cache_dir = str(Path.home() / ".lebit")
        
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / "username_cache.json"
        self._lock = Lock()
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize cache file if it doesn't exist
        if not self.cache_file.exists():
            self._write_cache({"usernames": []})

    def get_cached_usernames(self) -> List[str]:
        """
        Retrieve all cached usernames.

        Returns:
            List of cached usernames in order of storage.
        """
        try:
            data = self._read_cache()
            return data.get("usernames", [])
        except Exception as e:
            logger.error(f"Error reading username cache: {e}")
            return []

    def add_username(self, username: str) -> None:
        """
        Add a username to the cache if it doesn't already exist.
        Keeps only the most recent 5 usernames.

        Args:
            username: The username to add.
        """
        if not username or not isinstance(username, str):
            logger.warning("Invalid username provided to cache")
            return
        
        try:
            with self._lock:
                data = self._read_cache()
                usernames = data.get("usernames", [])
                
                # Prevent duplicates
                if username not in usernames:
                    usernames.insert(0, username)  # Add to front (most recent)
                    # Enforce max limit
                    if len(usernames) > self.MAX_CACHED_USERNAMES:
                        usernames = usernames[:self.MAX_CACHED_USERNAMES]
                    data["usernames"] = usernames
                    self._write_cache(data)
                    logger.debug(f"Added username '{username}' to cache")
        except Exception as e:
            logger.error(f"Error adding username to cache: {e}")

    def remove_username(self, username: str) -> None:
        """
        Remove a specific username from the cache.

        Args:
            username: The username to remove.
        """
        try:
            with self._lock:
                data = self._read_cache()
                usernames = data.get("usernames", [])
                
                if username in usernames:
                    usernames.remove(username)
                    data["usernames"] = usernames
                    self._write_cache(data)
                    logger.debug(f"Removed username '{username}' from cache")
        except Exception as e:
            logger.error(f"Error removing username from cache: {e}")

    def clear_all(self) -> None:
        """Clear all cached usernames."""
        try:
            with self._lock:
                self._write_cache({"usernames": []})
                logger.debug("Cleared all cached usernames")
        except Exception as e:
            logger.error(f"Error clearing username cache: {e}")

    def _read_cache(self) -> dict:
        """
        Read cache file atomically.

        Returns:
            Dictionary with cache data.
        """
        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return {"usernames": []}
        except json.JSONDecodeError:
            logger.warning(f"Cache file corrupted at {self.cache_file}, treating as empty")
            return {"usernames": []}

    def _write_cache(self, data: dict) -> None:
        """
        Write cache file atomically using temp file pattern.

        Args:
            data: Dictionary to write to cache.
        """
        temp_file = self.cache_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=2)
            # Atomic rename
            temp_file.replace(self.cache_file)
        except Exception as e:
            logger.error(f"Error writing username cache: {e}")
            # Clean up temp file if it exists
            try:
                temp_file.unlink()
            except Exception:
                pass
