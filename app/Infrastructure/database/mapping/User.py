from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.Domain.Entities.Base import EntityMeta

class User(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
