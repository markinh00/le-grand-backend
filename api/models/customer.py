from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    phone: str
    password: str

    addresses: list["Address"] = Relationship(back_populates="customer")

from api.models.address import Address
