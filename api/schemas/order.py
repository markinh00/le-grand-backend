from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from api.models.order import Card, Money, StateEnum
from api.schemas.address import AddressInOrderCreate, AddressInOrderRead
from api.schemas.customer import CustomerInOrder
from api.schemas.discount import DiscountInOrder
from api.schemas.product import ProductInOrderRead, ProductInOrderCreate
from api.schemas.pydantic_objectid import PydanticObjectId


class OrderCreate(BaseModel):
    customer: CustomerInOrder
    products: list[ProductInOrderCreate]
    discount_name: str | None = Field(default=None)
    total: float
    payment: Literal["pix"] | Card | Money


class DeliveryCreate(OrderCreate):
    address: AddressInOrderCreate
    delivery_fee: float = Field(ge=0)


class PickUpCreate(OrderCreate):
    date: datetime = Field(ge=datetime.now(ZoneInfo("America/Sao_Paulo")))


class OrderRead(BaseModel):
    id: PydanticObjectId
    customer: CustomerInOrder
    products: list[ProductInOrderRead]
    discount: DiscountInOrder | None = Field(default=None)
    total: float
    state: StateEnum
    created_at: datetime


class DeliveryRead(OrderRead):
    address: AddressInOrderRead
    delivery_fee: float = Field(ge=0)


class PickUpRead(OrderRead):
    date: datetime = Field(ge=datetime.now(ZoneInfo("America/Sao_Paulo")))


class OrderUpdate(BaseModel):
    add_product: list[ProductInOrderCreate] | None = Field(default=None)
    remove_product: list[ProductInOrderCreate] | None = Field(default=None)
    state: StateEnum | None = Field(default=None)


class DeliveryUpdate(OrderUpdate):
    address: AddressInOrderCreate | None = Field(default=None)


class PickUpUpdate(OrderUpdate):
    date: datetime | None = Field(default=None, ge=datetime.now(ZoneInfo("America/Sao_Paulo")))
