from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.application.app_services.ai_service import AIService
from app.infrastructure.security.jwt import authentication_request_handle
from app.application.dtos.openai import PromptRequest

router = APIRouter(prefix="/v1/ai", tags=["ai"])
protected_router = APIRouter(prefix="/v1/ai", tags=["ai"], dependencies=[Depends(authentication_request_handle)])

@protected_router.post("/prompt-gemini", status_code=status.HTTP_200_OK)
def generate(prompt_request: PromptRequest, 
             ai_service: AIService = Depends()):
    
    return StreamingResponse(ai_service.prompt_gemini(prompt_request.content), media_type="text/plain")