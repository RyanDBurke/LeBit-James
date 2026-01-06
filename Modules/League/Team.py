class Team:
    def __init__(self, user_id: str, display_name: str, avatar_id: str, nickname: str, is_commissioner: bool):
        self.user_id = user_id
        self.display_name = display_name
        self.avatar_id = avatar_id
        self.nickname = nickname
        self.is_commissioner = is_commissioner