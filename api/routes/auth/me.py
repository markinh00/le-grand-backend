from typing import Annotated
from fastapi import APIRouter, Security
from api.dependencies.auth import get_current_user
from api.schemas.user import UserScopes, User, UserRead

router = APIRouter(prefix="/auth/me", tags=["Auth"])


@router.get("/", response_model=UserRead)
def get_current_user(
        current_user: Annotated[User, Security(get_current_user, scopes=[UserScopes.CUSTOMER.value, UserScopes.ADMIN.value])]
):
    # user = UserRead(data=, scope=current_user.scope)
    return current_user
