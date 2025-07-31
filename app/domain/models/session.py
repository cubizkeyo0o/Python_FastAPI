from uuid import UUID, uuid4
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    JSON,
    CHAR,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database_init import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True, default=uuid4 ,index=True)
    user_id: Mapped[UUID] = mapped_column(CHAR(36), ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), index=True)
    summary_context: Mapped[str] = mapped_column(String(120), index=True, nullable=True)
    extra_metadata : Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)

    # reverse relationship to user
    user = relationship("UserDb", back_populates="sessions")

    # session 1-N message
    messages = relationship(
        "Message", back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Session {self.name}'