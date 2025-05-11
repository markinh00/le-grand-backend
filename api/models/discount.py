from typing import Optional
from sqlmodel import SQLModel, Field


class Discount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    value: int
    enabled: bool = True