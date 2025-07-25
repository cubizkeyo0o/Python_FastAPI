from fastapi import APIRouter, Depends, status, HTTPException, status, Path, Body, Query
from typing import List
from uuid import UUID

from app.infrastructure.security.jwt import authentication_request_handle
from app.application.app_services.message_service import MessageService
from app.application.dtos.message import *

router = APIRouter(prefix="/v1/message", tags=["message"])
protected_router = APIRouter(prefix="/v1/message", tags=["message"], dependencies=[Depends(authentication_request_handle)])

@protected_router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate = Body(...),
    message_service: MessageService = Depends()
):
    try:
        return await message_service.create_message(message_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected_router.get("/", response_model=List[MessageResponse])
async def list_messages(
    session_id: str = Query(..., description="Filter messages by session ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
    message_service: MessageService = Depends()
):
    try:
        return await message_service.get_messages(session_id=session_id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected_router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: UUID = Path(...),
    message_service: MessageService = Depends()
):
    try:
        message = await message_service.get_message(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected_router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: UUID = Path(...),
    message_data: MessageUpdate = Body(...),
    message_service: MessageService = Depends()
):
    try:
        updated = await message_service.update_message(message_id, message_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Message not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@protected_router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: UUID = Path(...),
    message_service: MessageService = Depends()
):
    try:
        deleted = await message_service.delete_message(message_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Message not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))