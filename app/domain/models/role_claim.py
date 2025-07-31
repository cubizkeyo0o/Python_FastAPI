from uuid import UUID
from sqlalchemy import String, ForeignKey, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.database_init import Base


class RoleClaim(Base):
    __tablename__ = "role_claims"

    id: Mapped[UUID] = mapped_column(CHAR(36), primary_key=True, index=True)
    role_id: Mapped[UUID] = mapped_column(CHAR(36), ForeignKey("roles.id", ondelete="CASCADE"))
    claim_type: Mapped[str] = mapped_column(String(50), nullable=False)
    claim_value: Mapped[str] = mapped_column(String(50), nullable=False)

    # N-1: RoleClaim belong 1 Role
    role = relationship("Role", back_populates="claims")