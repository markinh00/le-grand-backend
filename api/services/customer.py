from typing import List, Optional
from starlette.exceptions import HTTPException
from starlette import status
from api.models.customer import Customer
from api.repositories.customer import CustomerRepository
from api.schemas.customer import CustomerRegister, CustomerUpdate
from api.schemas.pagination import CustomerPagination
from api.services.db.database import get_session


class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository(session = next(get_session()) )

    def create_customer(self, customer_data: CustomerRegister) -> Customer:
        try:
            new_customer = Customer(
                name=customer_data.name,
                email=customer_data.email,
                phone=customer_data.phone,
                password=customer_data.password,
                addresses=[]
            )
            return self.repository.create(new_customer)
        except AttributeError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{error}"
            )
        except Exception as e:
            raise e

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.repository.get_by_id(customer_id)

    def get_customer_by_email(self, customer_email) -> Optional[Customer]:
        return self.repository.get_by_email(customer_email)

    def get_all_customers(self, query: CustomerPagination) -> List[Customer]:
        return self.repository.get_all(query)

    def update_customer(self, customer_id: int, updated_data: CustomerUpdate) -> Optional[Customer]:
        return self.repository.update(customer_id, updated_data)

    def delete_customer(self, customer_id: int) -> bool:
        return self.repository.delete(customer_id)
