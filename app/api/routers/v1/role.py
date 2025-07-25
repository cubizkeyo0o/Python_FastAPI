from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from uuid import UUID

from app.application.app_services.role_service import RoleService
from app.application.dtos.role import *
from app.utils.exceptions.common_exceptions import InternalServerErrorException

router = APIRouter(prefix="/v1/role", tags=["role"])

# GET all role
@router.get(
    "/",
    response_model=List[RoleResponse],
    status_code=status.HTTP_200_OK,
)
async def get_roles(role_service: RoleService = Depends()):
    try:
        roles_response = await role_service.get_all_async()
        return roles_response
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Don't get list role.",
        ) from ex

# Create new role
@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    role_create_request: RoleCreateRequest,
    role_service: RoleService = Depends(),
    ):
    response = await role_service.create_async(role_create_request.to_role_create())
    return response

# Update exist role
@router.patch(
    "/{id}",
    response_model=RoleResponse,
)
async def update(
    id: UUID,
    role_update: RoleUpdate,
    role_service: RoleService = Depends(),
):
    response = await role_service.update_async(id, role_update)
    return response

# delete exist role
@router.delete(
    "/{id}",
)
async def delete(
    id: UUID,
    role_service: RoleService = Depends(),
):
    delete_success = await role_service.delete_async(id)
    
    if not delete_success:
        raise InternalServerErrorException("Delete role failed")

    return {
        "success": True,
        "message": "Deleted successfully"
    }