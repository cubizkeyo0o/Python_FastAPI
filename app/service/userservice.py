from typing import List, Optional

from fastapi import Depends
from domain.user import User

from repositories.userrepository import userrepository

class userservice:
    userRepository: userrepository

    def __init__(
        self, userRepository: userrepository = Depends()
        ) -> None:
        self.userRepository = userrepository

    
