from typing import Optional
from pydantic import BaseModel


class AddressRead(BaseModel):
    id: int
    street: str
    number: int
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str

    customer_id: int

class AddressCreate(BaseModel):
    street: str
    number: int
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str

    customer_id: int

class AddressUpdate(BaseModel):
    street: str | None = None
    number: int  | None = None
    complement: str | None = None
    neighborhood: str  | None = None
    city: str  | None = None
    state: str  | None = None
    zip_code: str  | None = None
