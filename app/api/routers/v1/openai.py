from fastapi import APIRouter, Depends, status

from app.application.app_services.openai_service import OpenAIService
from app.infrastructure.security.jwt import authentication_request_handle
from app.application.dtos.openai import PromptRequest, PromptResponse

router = APIRouter(prefix="/v1/openai", tags=["openai"])
protected_router = APIRouter(prefix="/v1/openai", tags=["openai"], dependencies=[Depends(authentication_request_handle)])

@protected_router.post("/prompt", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def generate(prompt_request: PromptRequest,
                   openai_service: OpenAIService = Depends()):
    
    prompt_respone = await openai_service.generate_response(prompt_request.prompt)
    
    return PromptResponse(response=prompt_respone)