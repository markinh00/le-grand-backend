import os
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Security
from starlette.exceptions import HTTPException
from starlette import status
from api.schemas.jwt_token import Token
from api.schemas.customer import CustomerRegister
from api.schemas.user import UserScopes
from api.services.admin import AdminService
from api.services.customer import CustomerService
from api.dependencies.auth import create_access_token, get_password_hash, get_api_key

router = APIRouter(prefix="/auth/register", tags=["Auth"], dependencies=[Security(get_api_key)])

admin_service = AdminService()
user_service = CustomerService()

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

@router.post("/", response_model=Token)
def register_user(user_data: CustomerRegister) -> Token:
    try:
        if user_data.password != user_data.confirmPassword:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'password' and 'confirmPassword' must be the same value"
            )

        user_data.password = get_password_hash(user_data.password)

        result = user_service.create_customer(user_data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user_data.email} already exists!",
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": result.email, "scopes": [UserScopes.CUSTOMER.value]}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise e
