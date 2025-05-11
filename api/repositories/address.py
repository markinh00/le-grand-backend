from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from api.models.address import Address
from api.schemas.address import AddressUpdate


class AddressRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, address: Address) -> Address | None:
        try:
            self.session.add(address)
            self.session.commit()
            self.session.refresh(address)
            return address
        except IntegrityError:
            self.session.rollback()
            return None
        except Exception as e:
            raise e

    def get_by_id(self, address_id: int) -> Address | None:
        return self.session.get(Address, address_id)

    def update(self,address_id: int,  update_data: AddressUpdate) -> Address | None:
        address = self.get_by_id(address_id)

        if not address:
            return None

        for key, value in update_data.model_dump().items():
            if value is not None:
                setattr(address, key, value)

        self.session.add(address)
        self.session.commit()
        self.session.refresh(address)
        return address

    def delete(self, address_id: int) -> bool:
        address = self.get_by_id(address_id)

        if not address:
            return False

        self.session.delete(address)
        self.session.commit()
        return True