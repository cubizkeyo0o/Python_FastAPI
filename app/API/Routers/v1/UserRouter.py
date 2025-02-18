from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException
from app.Application.AppServices.UserAppService import UserService
from app.Application.Models.UserModel import (
    CreateUserModel,
    UpdateUserModel,
    ResponseUserModel
)

userrouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)

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


