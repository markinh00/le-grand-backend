from starlette import status
from starlette.exceptions import HTTPException
from api.models.address import Address
from api.models.customer import Customer
from api.repositories.address import AddressRepository
from api.schemas.address import AddressCreate, AddressUpdate
from api.services.db.sqlmodel.database import get_session


class AddressService:
    def __init__(self):
        self.repository = AddressRepository(session=next(get_session()))

    def create_address(self, new_address: AddressCreate):
        customer = self.repository.session.get(Customer, new_address.customer_id)

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {new_address.customer_id} not found"
            )

        try:
            address = Address(
                street=new_address.street,
                number=new_address.number,
                complement=new_address.complement,
                neighborhood=new_address.neighborhood,
                city=new_address.city,
                state=new_address.state,
                zip_code=new_address.zip_code,
                customer_id=new_address.customer_id
            )
            return self.repository.create(address)
        except AttributeError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{error}"
            )
        except Exception as e:
            raise e

    def get_address_by_id(self, address_id: int) -> Address | None:
        return self.repository.get_by_id(address_id)

    def update_address(self, address_id: int, update_data: AddressUpdate) -> Address | None:
        return self.repository.update(address_id, update_data)

    def delete_address(self, address_id: int) -> bool:
        return self.repository.delete(address_id)
