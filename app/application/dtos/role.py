from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class RoleBase(BaseModel):
    name: str
    normalized_name: str
    concurrency_stamp: str

class RoleCreate(BaseModel):
    name: str
    normalized_name: str = Field(default_factory=lambda: "", exclude=True)
    concurrency_stamp: str = Field(default_factory=lambda: str(uuid4()), exclude=True)

    @field_validator("name", mode="before")
    def to_model_dict(cls, v, values):
        if isinstance(v, str):
            values
        return v

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    concurrency_stamp: str 

    def get_updated_fields(self):
        updates = {}
        if self.name:
            updates["name"] = self.name
            updates["normalized_name"] = self.name.strip().upper()
        return updates

class RoleRead(RoleBase):
    id: UUID

    class Config:
        orm_mode = True
