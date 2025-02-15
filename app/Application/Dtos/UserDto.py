class UserDto:
    def __init__(self, user_id: int = 0, name: str = "", email: str = ""):
        self.user_id = user_id
        self.name = name
        self.email = email