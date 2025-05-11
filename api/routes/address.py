from typing import Annotated
from fastapi import APIRouter, Security
from starlette import status
from starlette.exceptions import HTTPException
from api.dependencies.auth import get_current_user
from api.schemas.Message import Message
from api.schemas.address import AddressRead, AddressCreate, AddressUpdate
from api.schemas.customer import CustomerRead
from api.schemas.user import UserScopes
from api.services.address import AddressService


router = APIRouter(prefix="/address", tags=["Address"])

service = AddressService()


@router.post("/", response_model=AddressRead)
def add_address_to_customer(
        new_address: AddressCreate,
        current_user: Annotated[CustomerRead, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    if current_user.data.id != new_address.customer_id and current_user.scope != UserScopes.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A customer cannot add an address to another customer"
        )

    return service.create_address(new_address)


@router.get("/{address_id}", response_model=AddressRead)
def get_address_dy_id(
        address_id: int,
        current_user: Annotated[CustomerRead, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    address = service.get_address_by_id(address_id)

    if current_user.data.id != address.customer_id and current_user.scope != UserScopes.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A customer does not have access to another customer's data"
        )

    return address


@router.put("/{address_id}", response_model=AddressRead)
def update_address(
        address_id: int,
        update_data: AddressUpdate,
        current_user: Annotated[CustomerRead, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    address = service.get_address_by_id(address_id)

    if current_user.data.id != address.customer_id and current_user.scope != UserScopes.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A customer does not have access to another customer's data"
        )

    updated = service.update_address(address_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    return updated


@router.delete("/{address_id}", response_model=Message)
def delete_address(
        address_id: int,
        current_user: Annotated[CustomerRead, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    address = service.get_address_by_id(address_id)

    if current_user.data.id != address.customer_id and current_user.scope != UserScopes.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A customer cannot delete another customer's data"
        )

    success = service.delete_address(address_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")


    return Message(detail="Customer deleted successfully")