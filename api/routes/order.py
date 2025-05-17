from typing import Annotated
from fastapi import APIRouter, Query, Security
from starlette import status
from starlette.exceptions import HTTPException
from api.dependencies.auth import get_current_user
from api.schemas.message import Message
from api.schemas.order import DeliveryCreate, PickUpCreate, DeliveryUpdate, PickUpUpdate, DeliveryRead, PickUpRead
from api.schemas.pagination import OrderPagination
from api.schemas.user import UserScopes, User
from api.services.order import OrderService

router = APIRouter(prefix="/order", tags=["Order"])

service = OrderService()


@router.post("/", response_model=DeliveryRead | PickUpRead)
def create_order(order_data: DeliveryCreate | PickUpCreate):
    return service.create_order(order_data)


@router.get(
    "/",
    response_model=list[DeliveryRead | PickUpRead],
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])])
def get_all_orders(query: Annotated[OrderPagination, Query()]):
    return service.repository.get_all(query)


@router.get(
    "/customer/{customer_id}",
    response_model=list[DeliveryRead | PickUpRead])
def get_customer_orders(
        customer_id: int,
        current_user: Annotated[
            User, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    if current_user.data.id != customer_id and current_user.scope == UserScopes.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A Customer cannot access another customer's data"
        )

    return service.get_customer_orders(customer_id)


@router.get(
    "/order_id",
    response_model=DeliveryRead | PickUpRead)
def get_order_by_id(
        order_id: str,
        current_user: Annotated[User, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    order = service.get_order_by_id(order_id)

    if order.customer.id != current_user.data.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A Customer cannot access another customer's data"
        )

    return order


@router.put(
    "/{order_id}",
    response_model=DeliveryRead | PickUpRead,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])])
def update_order(order_id: str, new_data: DeliveryUpdate | PickUpUpdate):
    return service.update_order(order_id, new_data)


@router.delete(
    "/{order_id}",
    response_model=Message,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])])
def delete_order(order_id: str):
    return service.delete_order(order_id)
