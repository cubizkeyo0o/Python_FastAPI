from uuid import UUID
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.database_init import Base


class RoleClaim(Base):
    __tablename__ = "role_claims"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    claim_type: Mapped[str] = mapped_column(String(50), nullable=False)
    claim_value: Mapped[str] = mapped_column(String(50), nullable=False)

    # N-1: RoleClaim belong 1 Role
    role = relationship("Role", back_populates="claims")