from fastapi import APIRouter, Depends, status, HTTPException
from app.Application.AppServices.UserAppService import UserService
from app.Application.Models.AuthModel import (
    LoginUserModel,
    RegisterUserModel,
    TokenResponseModel
)

authrouter = APIRouter(
    prefix="/v1/auth", tags=["auth"]
)

@authrouter.post('/login')
def login(request_data: LoginRequest):
    if verify_password(username=request_data.username, password=request_data.password):
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="User not found")
