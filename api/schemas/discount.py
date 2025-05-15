from pydantic import BaseModel, Field


class DiscountRead(BaseModel):
    id: int
    name: str
    value: int
    enabled: bool

class DiscountCreate(BaseModel):
    name: str
    value: int = Field(ge=0, le=100)
    enabled: bool | None = None

class DiscountUpdate(BaseModel):
    name: str | None = None
    value: int | None = None
    enabled: bool | None = None

class DiscountInOrder(BaseModel):
    id: int
    name: str
    value: int