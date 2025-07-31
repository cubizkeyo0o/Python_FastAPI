from uuid import UUID, uuid4
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    CHAR,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database_init import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True, default=uuid4 ,index=True)
    session_id: Mapped[UUID] = mapped_column(CHAR(36), ForeignKey("sessions.id"))
    role: Mapped[str] = mapped_column(String(255), index=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)

    # reverse relationship to session
    session = relationship("Session", back_populates="messages")

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Message {self.id}'