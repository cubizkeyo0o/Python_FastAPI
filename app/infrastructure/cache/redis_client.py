import redis
import json
import os
from typing import Any, Optional

from app.config import REDIS_URL, USERNAME_REDIS_CLOUD, PASSWORD_REDIS_CLOUD

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_URL,
            port=15756,
            decode_responses=True,
            username=USERNAME_REDIS_CLOUD,
            password=PASSWORD_REDIS_CLOUD,
        )