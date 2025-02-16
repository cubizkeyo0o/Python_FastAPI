from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from app.Infrastructure.database.mapping.Base import EntityMeta
from app.API.Models.UserModel import ResponseUserModel

class User(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)
    created = Column(DateTime, default=datetime.now)

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        
    def to_response(self) -> ResponseUserModel:
            return ResponseUserModel(id=self.id, name=self.name, email=self.email)
