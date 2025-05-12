from starlette import status
from starlette.exceptions import HTTPException

from api.models.discount import Discount
from api.repositories.discount import DiscountRepository
from api.schemas.discount import DiscountCreate, DiscountUpdate
from api.schemas.pagination import DiscountPagination
from api.services.db.sqlmodel.database import get_session


class DiscountService:
    def __init__(self):
        self.repository = DiscountRepository(session=next(get_session()))

    def create_discount(self, discount_data: DiscountCreate) -> Discount | None:
        try:
            new_discount = Discount(
                name=discount_data.name,
                value=discount_data.value,
                enabled=discount_data.enabled
            )
            return self.repository.create(new_discount)
        except AttributeError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{error}"
            )
        except Exception as e:
            raise e

    def get_all_discounts(self, query: DiscountPagination) -> list[Discount]:
        return self.repository.get_all(query)

    def get_discount_by_id(self, discount_id: int) -> Discount | None:
        return self.repository.get_by_id(discount_id)

    def get_discount_by_name(self, discount_name: str) -> Discount | None:
        return self.repository.get_by_name(discount_name)

    def update_discount(self, discount_id: int, update_data: DiscountUpdate) -> Discount | None:
        return self.repository.update(discount_id, update_data)

    def delete_discount(self, discount_id: int) -> bool:
        return self.repository.delete(discount_id)