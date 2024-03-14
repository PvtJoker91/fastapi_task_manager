from fastapi import APIRouter, Depends

from src.apps.auth.services import validate_auth_user, get_current_token_payload, get_current_active_auth_user
from src.api.v1.auth.schemas import TokenInfo
from src.apps.auth import utils as auth_utils
from src.api.v1.users.schemas import UserSchema


router = APIRouter(prefix="/auth", tags=["Auth JWT"])



@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
        "email": user.email,
        # "logged_in_at"
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
