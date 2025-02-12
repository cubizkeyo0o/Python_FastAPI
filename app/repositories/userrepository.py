from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from config.database import (
    get_db_connection,
)
from domain.user import User

class userrepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db
    
    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, id: int, user: User) -> User:
        user.id = id
        self.db.merge(user)
        self.db.commit()
        return user
