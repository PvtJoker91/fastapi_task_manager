from typing import Annotated

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.api.v1.auth import utils as auth_utils
from src.api.v1.users.dependencies import user_service_dependency
from src.api.v1.users.schemas import UserSchema
from src.apps.users.exceptions import UserNotFound
from src.apps.users.services import ORMUserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


async def validate_auth_user(
        service: Annotated[ORMUserService, Depends(user_service_dependency)],
        username: str = Form(),
        password: str = Form(),
) -> UserSchema:
    try:
        user = await service.get_user_by_username(username=username)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return UserSchema.from_entity(user)


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
            detail="invalid token error",
        )
    return payload



async def get_current_auth_user(
        service: Annotated[ORMUserService, Depends(user_service_dependency)],
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    try:
        user = await service.get_user_by_username(username=username)
        return UserSchema.from_entity(user)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
) -> UserSchema:
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
