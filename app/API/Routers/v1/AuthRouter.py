from fastapi import APIRouter, HTTPException
from app.Application.AppServices.UserAppService import UserService
from app.Application.AppServices.AuthService import AuthService
from app.Application.Models.AuthModel import (
    LoginUserModel
)

authrouter = APIRouter(
    prefix="/v1/auth", tags=["auth"]
)

@authrouter.post('/login')
def login(request_data: LoginUserModel):
    if AuthService.login_user(user_name=request_data.username, password=request_data.password):
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="User not found")