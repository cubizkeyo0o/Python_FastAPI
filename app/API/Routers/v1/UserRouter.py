from typing import List, Optional

from fastapi import APIRouter, Depends, status
from Application.AppServices import UserAppService
from Application.Dtos import UserDto
from Models.UserModel import (
    CreateUserModel,
    UpdateUserModel,
    ResponseUserModel,
)

userrouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)


@userrouter.post(
    "/",
    response_model=ResponseUserModel,
    status_code=status.HTTP_201_CREATED,
)
def create(
    user: CreateUserModel,
    userService: UserAppService = Depends(),
    ):
    return userService.create(UserDto()).normalize()


@userrouter.patch(
    "/{id}",
    response_model=ResponseUserModel,
    status_code=status.HTTP_201_CREATED,
)
def update(
    id: int,
    user: UpdateUserModel,
    userService: UserAppService = Depends(),
):
    return userService.update(id, UserDto(UpdateUserModel.name, UpdateUserModel.email)).normalize()
