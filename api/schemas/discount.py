from pydantic import BaseModel


class DiscountRead(BaseModel):
    id: int
    name: str
    value: int
    enabled: bool

class DiscountCreate(BaseModel):
    name: str
    value: int
    enabled: bool | None = None

class DiscountUpdate(BaseModel):
    name: str | None = None
    value: int | None = None
    enabled: bool | None = None
