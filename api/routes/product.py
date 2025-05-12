from typing import Annotated

from fastapi import APIRouter, Form, UploadFile, Query, Security
from starlette import status
from starlette.exceptions import HTTPException

from api.dependencies.auth import get_current_user
from api.schemas.message import Message
from api.schemas.pagination import ProductPagination
from api.schemas.product import ProductRead, ProductCreate, ProductUpdate
from api.schemas.user import UserScopes
from api.services.product import ProductService

router = APIRouter(prefix="/product", tags=["product"])

service = ProductService()

@router.post(
    "/",
    response_model=ProductRead,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])])
def create_product(
        img_file: UploadFile | None = None,
        name: str = Form(...),
        price: float = Form(...),
        category: str = Form(...),
        description: str = Form(...)
):
    new_product = ProductCreate(name=name, price=price, category=category, description=description, img_file=img_file)
    result = service.create_product(new_product)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="could not create the product"
        )

    return result

@router.get(
    "/",
    response_model=list[ProductRead],
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value, UserScopes.CUSTOMER.value])])
def get_all_products(query: Annotated[ProductPagination, Query()]):
    return  service.get_all_products(query)


@router.get(
    "/categories",
    response_model=list[str],
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value, UserScopes.CUSTOMER.value])])
def get_all_distinct_categories():
    return service.repository.get_all_categories()


@router.get(
    "/{product_id}",
    response_model=ProductRead | None,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value, UserScopes.CUSTOMER.value])])
def get_product_by_id(product_id: int):
    result = service.get_product_by_id(product_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return  result

@router.put(
    "/{product_id}",
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])])
def update_product(
        product_id: int,
        name: str | None = Form(default=None),
        price: float | None = Form(default=None),
        category: str | None = Form(default=None),
        description: str | None = Form(default=None),
        img_file: UploadFile | None = Form(default=None),
        delete_img: bool | None = Form(default=None),
):
    new_data = ProductUpdate(name=name, price=price, category=category, description=description,
                             img_file=img_file, delete_img=delete_img)

    updated = service.update_product(product_id, new_data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found")

    return updated


@router.delete(
    "/{product_id}",
    response_model=Message,
    dependencies=[Security(get_current_user, scopes=[UserScopes.ADMIN.value])])
def delete_product(product_id: int):
    success = service.delete_product(product_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found")

    return Message(detail="Product deleted successfully")