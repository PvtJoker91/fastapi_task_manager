from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.api.v1.users.schemas import UserSchema
from src.apps.auth import utils as auth_utils
from src.apps.users.entities import UserEntity
from src.apps.users.services import ORMUserService
from src.core.db import db_helper

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
) -> UserEntity:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    service = ORMUserService()
    if not (user := await service.get_user_by_username(session=db_helper.session_factory(), username=username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
) -> UserEntity:
    service = ORMUserService()
    username: str | None = payload.get("sub")
    if user := await service.get_user_by_username(session=db_helper.session_factory(), username=username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
        user: UserEntity = Depends(get_current_auth_user),
) -> UserEntity:
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
