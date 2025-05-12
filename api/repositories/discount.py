from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, desc
from api.models.discount import Discount
from api.schemas.discount import DiscountUpdate
from api.schemas.pagination import DiscountPagination


class DiscountRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, discount: Discount) -> Discount | None:
        try:
            self.session.add(discount)
            self.session.commit()
            self.session.refresh(discount)
            return discount
        except IntegrityError:
            self.session.rollback()
            return None
        except Exception as e:
            raise e

    def get_all(self, query: DiscountPagination) -> list[Discount]:
        statement = (select(Discount)
                     .offset((query.page - 1) * query.size)
                     .limit(query.size)
                     .order_by(desc(query.order.value) if query.desc else query.order.value))
        return list(self.session.exec(statement).all())

    def get_by_id(self, discount_id: int) -> Discount | None:
        return self.session.get(Discount, discount_id)

    def get_by_name(self, discount_name: str) -> Discount | None:
        try:
            statement = select(Discount).where(Discount.name == discount_name)
            return self.session.exec(statement).first()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, discount_id: int, update_data: DiscountUpdate) -> Discount | None:
        discount = self.get_by_id(discount_id)

        if not discount:
            return None

        for key, value in update_data.model_dump().items():
            if value is not None:
                setattr(discount, key, value)

        self.session.add(discount)
        self.session.commit()
        self.session.refresh(discount)
        return discount

    def delete(self, discount_id: int) -> bool:
        discount = self.get_by_id(discount_id)

        if not discount:
            return False

        self.session.delete(discount)
        self.session.commit()
        return True