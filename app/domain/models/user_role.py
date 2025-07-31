from uuid import UUID
from sqlalchemy import ForeignKey,CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database_init import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(CHAR(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(CHAR(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

    # N-1: UserRole belong 1 Role
    role = relationship("Role", back_populates="users")

    # N-1: UserRole belong 1 User
    user = relationship("UserDb", back_populates="roles")