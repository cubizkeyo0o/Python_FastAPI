from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Base Entity Model Schema
class Base(AsyncAttrs, DeclarativeBase):
    pass

EntityMeta = Base