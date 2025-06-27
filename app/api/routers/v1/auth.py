from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Response, Cookie
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer

from app.application.app_services.user_service import UserService
from app.application.dtos.auth import TokenPair, BlackListToken
from app.application.dtos.user import UserRegister, UserLogin, UserResponse

router = APIRouter(
    prefix="/v1/auth", tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post('/login')
async def login(
    request_data: UserLogin,
    user_service: UserService = Depends()
    ):
    if AuthService.login_user(user_name=request_data.user_name, password=request_data.password):
        return 'Success'
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.post('/register', response_model=UserResponse)
async def register(
    request_data: UserRegister,
    user_service: UserService = Depends()
    ):
    isExistAccountByUserN = await user_service.check_exist_user_name(name=request_data.user_name)
    if isExistAccountByUserN:
        raise HTTPException(status_code=400, detail="Username has already registered")

    isExistAccountByEmail = await user_service.check_exist_email(request_data.email)
    if isExistAccountByEmail:
        raise HTTPException(status_code=400, detail="Email has already registered")

    # create user
    create_user = await user_service.create_async(request_data)
    
    return create_user
