from enum import Enum

class KeyCache(str, Enum):
    SUMMARY_CONTEXT = "summary_context"
    RECENT_MESSAGES = "recent_messages"
    ROLE = "role"