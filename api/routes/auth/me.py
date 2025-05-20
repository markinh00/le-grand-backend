from typing import Annotated
from fastapi import APIRouter, Security
from api.dependencies.auth import get_current_user, get_api_key
from api.schemas.user import UserScopes, User, UserRead

router = APIRouter(prefix="/auth/me", tags=["Auth"], dependencies=[Security(get_api_key)])


@router.get("/", response_model=UserRead)
def get_current_user(
        current_user: Annotated[User, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
   return current_user
