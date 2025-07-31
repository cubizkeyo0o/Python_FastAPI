from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Column,
    DateTime,
    CHAR,
    func
)

from app.infrastructure.database.database_init import Base

class BlackListToken(Base):
    __tablename__ = "blacklist_tokens"

    id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True, default=uuid4 ,index=True)
    expire = Column(DateTime, server_default=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Token blacklisted ({self.id})'