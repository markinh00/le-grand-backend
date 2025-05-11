from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from api.models.customer import Customer


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    street: str
    number: int
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    customer_id: int = Field(foreign_key="customer.id")

    customer: Optional["Customer"] = Relationship(back_populates="addresses")