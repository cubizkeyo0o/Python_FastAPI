from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from uuid import UUID
from app.application.app_services.user_service import UserService
from app.application.dtos.user import UserResponse, UserRegister, UserUpdate

router = APIRouter(
    prefix="/v1/users", tags=["user"]
)

# GET all user
@router.get(
    "/",
    response_model=List[UserResponse],
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

# Create new user
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    user: UserRegister,
    user_service: UserService = Depends(),
    ):
    response = await user_service.create_async(user_register=user)
    return response

# Update exist user
@router.patch(
    "/{id}",
    response_model=UserResponse,
)
async def update(
    id: UUID,
    user: UserUpdate,
    user_service: UserService = Depends(),
):
    response = await user_service.update_async(user_id=id, user_body=user)
    return response

# delete exist user
@router.delete(
    "/{id}",
    response_model=UserResponse,
)
async def update(
    id: UUID,
    user_service: UserService = Depends(),
):
    response = await user_service.delete_async(user_id=id)
    return response
