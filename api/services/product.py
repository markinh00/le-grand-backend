import os

from api.models.product import Product
from api.repositories.product import ProductRepository
from api.schemas.pagination import ProductPagination
from api.schemas.product import ProductCreate, ProductRead, ProductUpdate
from api.services.db.sqlmodel.database import get_session
from api.services.db.image import upload_image


class ProductService:
    def __init__(self):
        self.repository = ProductRepository(session=next(get_session()))

    def create_product(self, new_product: ProductCreate) -> ProductRead | None:
        img_url = upload_image(img_file=new_product.img_file) if new_product.img_file else os.getenv("DEFAULT_IMAGE_URL")
        return self.repository.create(Product(
            name=new_product.name,
            price=new_product.price,
            description=new_product.description,
            category=new_product.category,
            img_url=img_url
        ))

    def get_all_products(self, query: ProductPagination) -> list[Product]:
        return self.repository.get_all(query)

    def get_all_categories(self) -> list[str]:
        return self.repository.get_all_categories()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.repository.get_by_id(product_id)

    def update_product(self, product_id: int, new_data: ProductUpdate):
        return self.repository.update(product_id, new_data)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)
