"""
Sleeper User
"""
from Modules.League.League import League


class User:
    def __init__(self, username: str, user_id: str, display_name: str, avatar_id: str, leagues: list[League] = None):
        self.username = username
        self.user_id = user_id
        self.display_name = display_name
        self.avatar_id = avatar_id
        self.leagues = leagues

    def __repr__(self):
        return f"User(username='{self.username}', user_id='{self.user_id}', display_name='{self.display_name}', avatar_id='{self.avatar_id}', leagues={self.leagues})"
