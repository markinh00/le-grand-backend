import re
from typing import Self
from pydantic import BaseModel, Field, model_validator
from starlette import status
from starlette.exceptions import HTTPException
from api.schemas.address import AddressRead


class CustomerRegister(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    confirmPassword:  str

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        self.phone = re.sub(r'\D', '', self.phone)
        if not len(self.phone) == 11 or  not self.phone[2] == '9':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number invalid"
            )
        return  self

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

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        self.phone = re.sub(r'\D', '', self.phone)
        if not len(self.phone) == 11 or not self.phone[2] == '9':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number invalid"
            )
        return self

class CustomerInOrder(BaseModel):
    id: int | None = Field(default=None)
    name: str
    phone: str
    email: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        self.phone = re.sub(r'\D', '', self.phone)
        if not len(self.phone) == 11 or not self.phone[2] == '9':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number invalid"
            )
        return self