from enum import Enum
from pydantic import BaseModel
from api.models.admin import Admin
from api.models.customer import Customer
from api.schemas.admin import AdminRead
from api.schemas.customer import CustomerRead


class UserScopes(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(BaseModel):
    data: Admin | Customer
    scope: UserScopes

class UserRead(BaseModel):
    data: AdminRead | CustomerRead
    scope: UserScopes