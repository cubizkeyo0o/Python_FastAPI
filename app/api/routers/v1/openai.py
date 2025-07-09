from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.utils.exceptions.http_exceptions import NotFoundException
from app.application.app_services.openai_service import OpenAIService
from app.application.app_services.auth_service import AuthService
from app.application.app_services.user_service import UserService
from app.application.dtos.openai import PromptRequest, PromptResponse

router = APIRouter(prefix="/v1/openai", tags=["openai"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/prompt", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def generate(token: Annotated[str, Depends(oauth2_scheme)],
                   prompt_request: PromptRequest,
                   openai_service: OpenAIService = Depends(),
                   auth_service: AuthService = Depends(),
                   user_service: UserService = Depends()):

    payload = await auth_service.check_access_token(token_check=token)

    user = await user_service.get_by_id_async(payload.subject)
    if not user:
        raise NotFoundException(detail="User not found")
    
    prompt_respone = await openai_service.generate_response(prompt_request.prompt)
    
    return PromptResponse(response=prompt_respone)