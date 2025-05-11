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
