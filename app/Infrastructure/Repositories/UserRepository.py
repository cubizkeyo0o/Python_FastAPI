from typing import List, Optional
from asyncio import wait

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from app.Infrastructure.database.DatabaseInit import (
    get_db_connection,
)
from app.Domain.Entities.User import CreateUserRequest, User
from app.Infrastructure.database.mapping import User as userRepository
from app.API.Models.UserModel import ResponseUserModel

class UserRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db
    
    def create(self, user_request: CreateUserRequest) -> ResponseUserModel:
        user_create = userRepository(user_request.name, user_request.email)
        self.db.add(user_create)
        self.db.commit()
        self.db.refresh(user_create)
        return user_create
    
    def update(self, id: int, user: User) -> ResponseUserModel:
        user.id = id
        self.db.merge(user)
        self.db.commit()
        return user
