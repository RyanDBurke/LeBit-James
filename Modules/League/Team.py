class Team:
    def __init__(self, league_id: str, user_id: str, display_name: str, avatar_id: str, nickname: str,
                 is_commissioner: bool):
        self.league_id = league_id
        self.user_id = user_id  # functions as team_id
        self.display_name = display_name
        self.avatar_id = avatar_id
        self.nickname = nickname
        self.is_commissioner = is_commissioner
