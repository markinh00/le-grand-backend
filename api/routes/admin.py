from fastapi import APIRouter, Security
from starlette import status
from starlette.exceptions import HTTPException
from api.dependencies.auth import get_current_user
from api.schemas.admin import AdminRead, AdminRegister, AdminUpdate
from api.schemas.message import Message
from api.schemas.user import UserScopes
from api.services.admin import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Security(get_current_user, scopes=UserScopes.ADMIN.value)]
)

service = AdminService()

@router.post("/", response_model=AdminRead)
def create_admin(admin_data: AdminRegister):
    return service.create_admin(admin_data)

@router.get("/{admin_id}", response_model=AdminRead)
def get_admin_by_id(admin_id: int):
    return service.get_admin_by_id(admin_id)

@router.put("/{admin_id}", response_model=AdminRead)
def update_admin(admin_id: int, update_data: AdminUpdate):
    updated = service.update_admin(admin_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )

    return updated

@router.delete("/{admin_id}", response_model=Message)
def delete_admin(admin_id: int):
    success = service.delete_admin(admin_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")

    return Message(detail="Customer deleted successfully")