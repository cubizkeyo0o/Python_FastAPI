from typing import List, Optional
from asyncio import wait

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from app.Infrastructure.database.DatabaseInit import (
    get_db_connection,
)
from app.Infrastructure.database.mapping.User import User

class UserRepository:
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
