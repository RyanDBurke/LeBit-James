import json
import logging
from pathlib import Path
from typing import List, Dict
from threading import Lock
from datetime import datetime

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

    def get_cached_usernames(self) -> List[Dict]:
        """
        Retrieve all cached usernames sorted by favorite status and last login date.

        Returns:
            List of cached username dictionaries with metadata, sorted by favorite first, then by last login date.
        """
        try:
            data = self._read_cache()
            usernames = data.get("usernames", [])
            # Sort: favorites first, then by last_login_date (newest first)
            sorted_usernames = sorted(
                usernames,
                key=lambda x: (not x.get("is_favorite", False), -datetime.fromisoformat(x.get("last_login", "1970-01-01T00:00:00")).timestamp())
            )
            return sorted_usernames
        except Exception as e:
            logger.error(f"Error reading username cache: {e}")
            return []



    def _enforce_cache_limit(self, usernames: List[Dict]) -> List[Dict]:
        """
        Enforce the cache limit by removing excess usernames.
        Prioritizes removing oldest non-favorite usernames first.
        If all are favorites, removes the oldest username.

        Args:
            usernames: List of username dictionaries

        Returns:
            trimmed list or usernames
        """
        while len(usernames) > self.MAX_CACHED_USERNAMES:
            # Find oldest non-favorite username
            non_favorites = [u for u in usernames if not u.get("is_favorite", False)]
            
            if non_favorites:
                # Remove the oldest non-favorite (last in list since it's sorted by date desc)
                oldest_non_fav = non_favorites[-1]
                usernames = [u for u in usernames if u.get("username") != oldest_non_fav.get("username")]
            else:
                # All are favorites, remove the oldest one
                usernames = usernames[:-1]
        
        return usernames

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
                # Check if username already exists
                existing_user = next((u for u in usernames if u.get("username") == username), None)
                if existing_user:
                    # Update last login date
                    existing_user["last_login"] = datetime.now().isoformat()
                else:
                    # Add new user
                    usernames.insert(0, {
                        "username": username,
                        "is_favorite": False,
                        "last_login": datetime.now().isoformat()
                    })
                    # Enforce max limit with smart removal
                    usernames = self._enforce_cache_limit(usernames)
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
                usernames = [u for u in usernames if u.get("username") != username]
                data["usernames"] = usernames
                self._write_cache(data)
                logger.debug(f"Removed username '{username}' from cache")
        except Exception as e:
            logger.error(f"Error removing username from cache: {e}")

    def toggle_favorite(self, username: str) -> None:
        """
        Toggle the favorite status of a username.

        Args:
            username: The username to toggle.
        """
        try:
            with self._lock:
                data = self._read_cache()
                usernames = data.get("usernames", [])
                user = next((u for u in usernames if u.get("username") == username), None)
                if user:
                    user["is_favorite"] = not user.get("is_favorite", False)
                    data["usernames"] = usernames
                    self._write_cache(data)
                    logger.debug(f"Toggled favorite status for '{username}' to {user['is_favorite']}")
        except Exception as e:
            logger.error(f"Error toggling favorite: {e}")

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
