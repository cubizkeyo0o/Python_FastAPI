from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database_init import Base

class BlackListToken(Base):
    __tablename__ = "blacklist_tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4 ,index=True)
    expire: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)