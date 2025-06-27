from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import UUID4

from app.infrastructure.database.database_init import Base

class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[UUID4] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    user_name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'User({self.id}, "{self.name}")'