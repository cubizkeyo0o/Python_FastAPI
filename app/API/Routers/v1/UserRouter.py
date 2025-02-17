from typing import List, Optional

from fastapi import APIRouter, Depends, status
from app.Application.AppServices.UserAppService import UserService
from app.Application.Dtos.UserDto import UserDto
from app.API.Models.UserModel import (
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
    return userService.create(UserDto(user.name, user.email))


@userrouter.patch(
    "/{id}",
    response_model=ResponseUserModel,
    status_code=status.HTTP_201_CREATED,
)
async def update(
    id: int,
    user: UpdateUserModel,
    userService: UserService = Depends(),
):
    return userService.update(id, UserDto(user.name, user.email))


