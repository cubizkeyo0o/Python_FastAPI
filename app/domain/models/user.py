from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    DateTime,
    CHAR
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database_init import Base

class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True, default=uuid4 ,index=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    user_name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # user 1-N session
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

    # user 1-N user_roles
    roles = relationship("UserRole", back_populates="user")

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'User {self.name}'