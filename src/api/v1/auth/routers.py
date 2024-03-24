from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.v1.auth import utils as auth_utils
from src.api.v1.auth.dependencies import validate_auth_user, get_current_token_payload, get_current_active_auth_user
from src.api.v1.auth.schemas import TokenInfo
from src.api.v1.users.dependencies import user_service_dependency
from src.api.v1.users.schemas import UserSchema, UserCreateSchema
from src.apps.users.exceptions import UserAlreadyExists
from src.apps.users.services import ORMUserService

router = APIRouter(prefix="/auth", tags=["Auth JWT"])


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(
        user: UserCreateSchema,
        user_service: Annotated[ORMUserService, Depends(user_service_dependency)]
):
    try:
        user = await user_service.create_user(user.to_entity())
        return UserSchema.from_entity(user)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={"message": e.message})


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/me/")
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
