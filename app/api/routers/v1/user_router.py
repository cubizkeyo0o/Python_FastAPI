from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.application.app_services.user_service import UserService
from app.application.models.user_model import (
    CreateUserModel,
    UpdateUserModel,
    ResponseUserModel
)

userrouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)

# GET all user
@userrouter.get(
    "/",
    response_model=List[ResponseUserModel],
    status_code=status.HTTP_200_OK,
)
async def get_users(user_service: UserService = Depends()):
    try:
        users = await user_service.get_all_async()
        return users
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Don't get list user.",
        ) from ex

@userrouter.post(
    "/",
    response_model=ResponseUserModel,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    user: CreateUserModel,
    userService: UserService = Depends(),
    ):
    try:
        response = await userService.create_async(user_body=user)
        return response
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from ex


@userrouter.patch(
    "/{id}",
    response_model=ResponseUserModel,
)
async def update(
    id: int,
    user: UpdateUserModel,
    userService: UserService = Depends(),
):
    try:
        response = await userService.update_async(id, user_body=user)
        return response
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from ex


