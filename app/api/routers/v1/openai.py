from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from fastapi.responses import StreamingResponse

from app.application.app_services.ai_service import AIService
from app.application.app_services.session_service import SessionService
from app.infrastructure.security.jwt import authentication_request_handle
from app.utils.exceptions.common_exceptions import EntityNotFoundException
from app.application.dtos.openai import PromptRequest

router = APIRouter(prefix="/v1/ai", tags=["ai"])
protected_router = APIRouter(prefix="/v1/ai", tags=["ai"], dependencies=[Depends(authentication_request_handle)])

@protected_router.post("/prompt-gemini", status_code=status.HTTP_200_OK)
async def generate(prompt_request: PromptRequest, 
                   request_http: Request,
                   background_tasks: BackgroundTasks,
                   ai_service: AIService = Depends(),
                   session_service: SessionService = Depends()):
    # get role of user
    user_roles = request_http.state.roles
    user_role = user_roles[0] if user_roles else ""

    # check session
    session_exist = await session_service.get_session(prompt_request.session_id)
    if not session_exist:
        raise EntityNotFoundException("Session not found")

    # count recent messages to summary
    count_messages = await session_service.count_messages_by_session(prompt_request.session_id)

    # check if first message or message 10, 20, ...
    if count_messages == 0 or count_messages % 10 == 0:
        # run back ground task to generate summary context and title
        background_tasks.add_task(ai_service.generate_summary_context, prompt_request.session_id)
        background_tasks.add_task(ai_service.generate_title_session, prompt_request.session_id)

    return StreamingResponse((ai_service.prompt_gemini(session_id=prompt_request.session_id, role=user_role, content=prompt_request.content)), media_type="text/plain")