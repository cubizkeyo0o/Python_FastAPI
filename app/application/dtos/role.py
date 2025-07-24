from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import UUID, uuid4

class RoleBase(BaseModel):
    name: str
    normalized_name: str
    concurrency_stamp: str

class RoleCreate(BaseModel):
    name: str
    normalized_name: str
    concurrency_stamp: str

class RoleCreateRequest(BaseModel):
    name: str

    def to_role_create(self) -> RoleCreate:
        return RoleCreate(
            name=self.name,
            normalized_name=self.name.upper(),
            concurrency_stamp=str(uuid4())
        )

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    concurrency_stamp: str 

    def get_updated_fields(self):
        updates = {}
        if self.name:
            updates["name"] = self.name
            updates["normalized_name"] = self.name.strip().upper()
        return updates

class RoleResponse(RoleBase):

    class Config:
        from_attributes = True
