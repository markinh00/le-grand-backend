from typing import Annotated
from fastapi import APIRouter, Query, Security
from starlette import status
from starlette.exceptions import HTTPException
from api.dependencies.auth import get_current_user
from api.schemas.message import Message
from api.schemas.discount import DiscountCreate, DiscountRead, DiscountUpdate
from api.schemas.pagination import DiscountPagination
from api.schemas.user import UserScopes
from api.services.discount import DiscountService


router = APIRouter(prefix="/discount", tags=["Discount"])

service = DiscountService()

@router.post(
    "/",
    response_model=DiscountRead,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])]
)
def create_discount(discount_data: DiscountCreate):
    return service.create_discount(discount_data)


@router.get(
    "/",
    response_model=list[DiscountRead],
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])]
)
def get_all_customers(query: Annotated[DiscountPagination, Query()]):
    return service.get_all_discounts(query)


@router.get(
    "/name/{discount_name}",
    response_model=DiscountRead,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value, UserScopes.CUSTOMER.value])]
)
def get_discount_by_name(discount_name: str):
    result = service.get_discount_by_name(discount_name)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discount not found"
        )

    return  result


@router.get(
    "/{discount_id}",
    response_model=DiscountRead,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])]
)
def get_discount_by_id(discount_id: int):
    result = service.get_discount_by_id(discount_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discount not found"
        )

    return  result


@router.put(
    "/{discount_id}",
    response_model=DiscountRead,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])]
)
def update_discount(discount_id: int, update_data: DiscountUpdate):
    updated = service.update_discount(discount_id, update_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discount not found")

    return updated


@router.delete(
    "/{discount_id}",
    response_model=Message,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])]
)
def delete_product(discount_id: int):
    success = service.delete_discount(discount_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discount not found")

    return Message(detail="Discount deleted successfully")