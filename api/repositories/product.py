import os
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, desc, distinct
from api.models.product import Product
from api.schemas.pagination import ProductPagination
from api.schemas.product import ProductUpdate
from api.services.db.image_storage import upload_image, delete_image


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, product: Product) -> Product | None:
        try:
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return product
        except IntegrityError as e:
            self.session.rollback()
            return None
        except Exception as e:
            raise e

    def get_all(self, query: ProductPagination) -> list[Product]:
        statement = (
            select(Product)
            .offset((query.page - 1) * query.size)
            .limit(query.size)
            .order_by(desc(query.order.value) if query.desc else query.order.value)
        )
        return list(self.session.exec(statement).all())

    def get_all_categories(self) -> list[str]:
        statement = select(distinct(Product.category))
        return list(self.session.exec(statement).all())

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def update(self, product_id: int, new_data: ProductUpdate) -> Product | None:
        product = self.get_by_id(product_id)

        if not product:
            return None

        for key, value in new_data.model_dump().items():
            if value:
                if key == "delete_img":
                    delete_image(product.img_url)
                    product.img_url = os.getenv("DEFAULT_IMAGE_URL")

                elif key == "img_file":
                    delete_image(product.img_url)
                    img_url: str = upload_image(value)
                    product.img_url = img_url

                else:
                    setattr(product, key, value)

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: int):
        product = self.get_by_id(product_id)

        if not product:
            return False

        delete_image(product.img_url)

        self.session.delete(product)
        self.session.commit()
        return True