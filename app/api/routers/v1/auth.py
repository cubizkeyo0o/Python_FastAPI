from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.application.app_services.user_service import UserService
from app.application.app_services.auth_service import AuthService
from app.application.dtos.auth import TokenPairRegisterResponse
from app.application.dtos.user import UserRegister, UserLogin
from app.utils.exceptions.http_exceptions import InternalServerErrorException

router = APIRouter(
    prefix="/v1/auth", tags=["auth"]
)

@router.post('/login')
async def login(
    response: Response,
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
    ):
    username = form_data.username
    password = form_data.password
    user_login = UserLogin(user_name=username, password=password)
    login_succes_user = await user_service.login_account(user_login)

    if not login_succes_user:
        raise InternalServerErrorException()

    token_pair = auth_service.generate_token_pair(login_succes_user.id)

    auth_service.add_refresh_token_cookie(response, token_pair.refresh_token)

    return {
            "access_token": token_pair.access_token,
            "token_type": "bearer"
            }

    
@router.post('/register', response_model=TokenPairRegisterResponse)
async def register(
    request_data: UserRegister,
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends()
    ):
    isExistAccountByUserN = await user_service.check_exist_user_name(name=request_data.user_name)
    if isExistAccountByUserN:
        raise HTTPException(status_code=400, detail="Username has already registered")

    isExistAccountByEmail = await user_service.check_exist_email(request_data.email)
    if isExistAccountByEmail:
        raise HTTPException(status_code=400, detail="Email has already registered")

    # create user
    create_user = await user_service.create_async(request_data)
    
    # generate token
    token_pair = auth_service.generate_token_pair(user_id=create_user.id)
    
    return TokenPairRegisterResponse(access_token=token_pair.access_token, refresh_token=token_pair.refresh_token, user=create_user)
