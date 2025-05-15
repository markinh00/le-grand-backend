from pydantic import BaseModel, Field
from enum import Enum


class Pagination(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=10, le=100)
    desc: bool | None = Field(default=None)

class CustomerOrderEnum(Enum):
    ID = "id"
    NAME = "name"
    PHONE = "phone"
    EMAIL = "email"

class CustomerPagination(Pagination):
    order: CustomerOrderEnum = Field(default=CustomerOrderEnum.NAME)

class ProductOrderEnum(Enum):
    ID = "id"
    NAME = "name"
    PRICE = "price"
    DESCRIPTION = "description"
    CATEGORY = "category"
    IMG = "img_url"

class ProductPagination(Pagination):
    order: ProductOrderEnum = Field(default=ProductOrderEnum.NAME)

class DiscountOrderEnum(Enum):
    ID = "id"
    NAME = "name"
    VALUE = "value"
    ENABLED = "enabled"

class DiscountPagination(Pagination):
    order: DiscountOrderEnum = Field(default=DiscountOrderEnum.NAME.value)

class OrdersOrderEnum(Enum):
    ID = "_id"
    CUSTOMER_NAME = "customer.name"
    DISCOUNT_NAME = "discount.name"
    DISCOUNT_VALUE = "discount.value"
    TOTAL = "total"
    CREATED_AT = "created_at"

class OrderPagination(Pagination):
    order: OrdersOrderEnum = Field(default=OrdersOrderEnum.CREATED_AT)