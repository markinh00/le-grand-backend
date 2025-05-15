from datetime import datetime
from enum import Enum
from typing import Self, Literal
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, model_validator
from starlette import status
from starlette.exceptions import HTTPException
from api.schemas.address import AddressInOrderRead
from api.schemas.customer import CustomerInOrder
from api.schemas.discount import DiscountInOrder
from api.schemas.product import ProductInOrderRead
from api.schemas.pydantic_objectid import PydanticObjectId


class Money(BaseModel):
    change_for: float = Field(ge=0)


class Card(BaseModel):
    card: Literal["credit", "debit"]


class StateEnum(Enum):
    CANCELED = "canceled"
    AWAITING = "awaiting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class Order(BaseModel):
    id: PydanticObjectId | None = Field(alias="_id", default=None)
    customer: CustomerInOrder
    products: list[ProductInOrderRead]
    discount: DiscountInOrder | None = Field(default=None)
    total: float
    payment: Literal["pix"] | Card | Money
    state: StateEnum = Field(default=StateEnum.AWAITING)
    created_at: datetime = datetime.now(ZoneInfo("America/Sao_Paulo"))

    def to_pymongo(self):
        order: dict = self.model_dump()
        order.pop("id")
        order["state"] = self.state.value
        return order

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        self.total = round(self.total, 2)

        if isinstance(self.payment, Money):
            if self.payment.change_for < self.total:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Change '{self.payment.change_for}' must be equal or greater than total price {self.total}"
                )

        return self


class Delivery(Order):
    address: AddressInOrderRead
    delivery_fee: float = Field(ge=0)

    @model_validator(mode="after")
    def fill_fields(self) -> Self:
        self.total = round(self.total, 2)
        total = self.delivery_fee

        for product in self.products:
            total += (product.price * product.quantity)

            total = round(total, 2)

        if self.discount and self.discount.value > 0:
            total *= (1 - (self.discount.value / 100))
            total = round(total, 2)

        if total != self.total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the total price was miscalculated"
            )

        return self


class PickUp(Order):
    date: datetime = Field(ge=datetime.now())

    @model_validator(mode="after")
    def fill_fields(self) -> Self:
        self.total = round(self.total, 2)
        total = 0

        for product in self.products:
            total += (product.price * product.quantity)
            total = round(total, 2)

        if self.discount and self.discount.value > 0:
            total *= (1 - (self.discount.value / 100))
            total = round(total, 2)

        if total != self.total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the total price was miscalculated"
            )

        return self
