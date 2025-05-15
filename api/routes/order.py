from typing import Annotated
from fastapi import APIRouter, Query
from api.schemas.message import Message
from api.schemas.order import DeliveryCreate, PickUpCreate, DeliveryUpdate, PickUpUpdate, DeliveryRead, PickUpRead
from api.schemas.pagination import OrderPagination
from api.services.order import OrderService

router = APIRouter(prefix="/order", tags=["Order"])

service = OrderService()

@router.post("/", response_model=DeliveryRead | PickUpRead)
def create_order(order_data: DeliveryCreate | PickUpCreate):
    return service.create_order(order_data)

@router.get("/", response_model=list[DeliveryRead | PickUpRead])
def get_all_orders(query: Annotated[OrderPagination, Query()]):
    return service.repository.get_all(query)

@router.get("/customer/{customer_id}", response_model=list[DeliveryRead | PickUpRead])
def get_customer_orders(customer_id: int):
    return service.get_customer_orders(customer_id)

@router.get("/order_id", response_model=DeliveryRead | PickUpRead)
def get_order_by_id(order_id: str):
    return service.get_order_by_id(order_id)

@router.put("/{order_id}", response_model=DeliveryRead | PickUpRead)
def update_order(order_id: str, new_data: DeliveryUpdate | PickUpUpdate):
    return service.update_order(order_id, new_data)

@router.delete("/{order_id}", response_model=Message)
def delete_order(order_id: str):
    return service.delete_order(order_id)
