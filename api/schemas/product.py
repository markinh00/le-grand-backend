from typing import Self
from fastapi import UploadFile
from pydantic import BaseModel, model_validator, Field
from starlette import status
from starlette.exceptions import HTTPException


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    category: str
    img_file: UploadFile | None = Field(default=None)

    @model_validator(mode="after")
    def validate_file_type(self) -> Self:
        self.price = round(self.price, 2)
        if self.img_file and not self.img_file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file must be an image."
            )
        return self


class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str
    img_url: str

    class Config:
        from_attributes = True


class ProductSearchParams(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    price: float | None = Field(default=None)
    category: str | None = Field(default=None)
    img_url: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_field(self) -> Self:
        counter: int = 0
        for field, _ in self.model_dump().items():
            if self.model_dump()[field] is not None:
                counter = counter + 1
            if counter >= 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="only one parameter can be used for search!"
                )
        if counter == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="a parameter is needed for the search!"
            )
        return self


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None)
    price: float | None = Field(default=None)
    category: str | None = Field(default=None)
    description: str | None = Field(default=None)
    img_file: UploadFile | None = Field(default=None)
    delete_img: bool | None = Field(default=None)

    @model_validator(mode="after")
    def validate_field(self) -> Self:
        if self.img_file and not self.img_file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file must be an image."
            )
        print("self.img_file and self.delete_img:", self.img_file and self.delete_img)
        if self.img_file and self.delete_img:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="deleting and updating a image is not possible!"
            )
        return self


class ProductInOrderCreate(BaseModel):
    id: int
    quantity: int


class ProductInOrderRead(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str
    img_url: str
    quantity: int
