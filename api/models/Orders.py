from pydantic import BaseModel
from api.schemas.customer import CustomerRead
from api.schemas.product import ProductInOrder


class Orders(BaseModel):
    id: int
    customer: CustomerRead
    products: list[ProductInOrder]
