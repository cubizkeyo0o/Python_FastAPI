from pydantic import BaseModel, EmailStr


# Domain model for a User
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id  # User ID
        self.name = name  # User name
        self.email = email  # User email

# Pydantic model for creating a new user request
class CreateUserRequest(BaseModel):
    name: str  # Name of the user
    email: EmailStr  # Email of the user, validated as an email string


# Pydantic model for the response after creating a new user
class CreateUserResponse(BaseModel):
    id: int  # User ID
    name: str  # Name of the user
    email: EmailStr  # Email of the user, validated as an email string

    class Config:
        from_attributes = True  # Enable population of the model from attributes
