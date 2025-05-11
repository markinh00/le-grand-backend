from pydantic import BaseModel
from api.schemas.address import AddressRead


class CustomerRegister(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    confirmPassword:  str

class CustomerRead(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    addresses: list[AddressRead]

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None