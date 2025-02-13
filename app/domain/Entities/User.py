from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
)

from Base import EntityMeta

class User(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer)
    name = Column(String(16), nullable=False)
    email = Column(String(32), nullable=False)

    PrimaryKeyConstraint(id)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }
