import os
from datetime import timedelta
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException
from api.schemas.jwt_token import Token
from api.dependencies.auth import authenticate_user, create_access_token, get_api_key

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(prefix="/auth/login", tags=["Auth"], dependencies=[Security(get_api_key)])

@router.post("/", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.data.email, "scopes": [user.scope.value]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
