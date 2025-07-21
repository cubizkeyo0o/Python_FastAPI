from fastapi import APIRouter, Depends, status, HTTPException, status, Path, Body

from app.infrastructure.security.jwt import authentication_request_handle
from app.application.app_services.session_service import SessionService
from app.application.dtos.session import *

router = APIRouter(prefix="/v1/session", tags=["session"])
protected_router = APIRouter(prefix="/v1/session", tags=["session"], dependencies=[Depends(authentication_request_handle)])

@protected_router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate = Body(...),
    session_service: SessionService = Depends()
):
    return await session_service.create_session(session_data)

@protected_router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str = Path(...),
    session_service: SessionService = Depends()
):
    try:
        session = await session_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected_router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str = Path(...),
    session_data: SessionUpdate = Body(...),
    session_service: SessionService = Depends()
):
    try:
        updated = await session_service.update_session(session_id, session_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Session not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected_router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str = Path(...),
    session_service: SessionService = Depends()
):
    try:
        deleted = await session_service.delete_session(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))