from fastapi import APIRouter, HTTPException
from app.application.app_services.auth_service import AuthService
from app.application.models.auth_model import (
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