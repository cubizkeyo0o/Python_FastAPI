from enum import Enum

class SystemRole(str, Enum):
    ADMIN = "Admin"
    USER = "User"
    MANAGER = "Manager"
    GUEST = "Guest"
    ASSISTANT = "Assistant"
    MODEL="Model"

    @property
    def normalized(self) -> str:
        return self.value.upper()