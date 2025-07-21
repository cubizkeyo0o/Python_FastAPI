from uuid import UUID, uuid4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.database_init import Base

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    normalized_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    concurrency_stamp: Mapped[str] = mapped_column(String(50), nullable=True)

    # role 1-N roleclaim
    claims = relationship("RoleClaim", back_populates="role", cascade="all, delete-orphan")
    
    # role 1-N userroles
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")