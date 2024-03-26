from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from orjson import orjson
from punq import Container
from sqlalchemy.ext.asyncio import AsyncSession

from project.containers import get_container
from src.api.v1.auth.dependencies import auth_service_dependency
from src.api.v1.auth.schemas import TokenSchema, TokenPayloadSchema
from src.api.v1.users.dependencies import user_service_dependency
from src.api.v1.users.schemas import UserSchema, UserCreateSchema
from src.apps.common.exceptions import ServiceException
from src.apps.users.entities.users import UserEntity
from src.apps.users.exceptions.users import UserAlreadyExists
from src.apps.users.services.auth import BaseAuthService
from src.apps.users.services.users import ORMUserService
from src.apps.users.use_cases.auth import IssueTokenUseCase
from src.db.db_helper import db_helper

router = APIRouter(prefix="/auth", tags=["Auth JWT"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(
        user: UserCreateSchema,
        user_service: ORMUserService = Depends(user_service_dependency),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        user = await user_service.create_user(user.to_entity(), session=session)
        return UserSchema.from_entity(user)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={"message": e.message})


@router.post("/login/", response_model=TokenSchema)
async def auth_user_issue_jwt(
        username: str = Form(),
        password: str = Form(),
        container: Container = Depends(get_container),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    use_case: IssueTokenUseCase = container.resolve(IssueTokenUseCase)
    user: UserEntity = UserEntity(username=username, password=password)
    try:
        token = await use_case.execute(user_in=user, session=session)
    except ServiceException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg="User could not authenticate", extra={"error_meta": orjson.dumps(exception).decode()})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        ) from exception

    return TokenSchema.from_entity(token)


@router.get("/me/")
def auth_user_check_self_info(
        token: str = Depends(oauth2_scheme),
        service: BaseAuthService = Depends(auth_service_dependency)
):
    try:
        payload = service.get_user_from_token(token)
    except ServiceException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        ) from exception

    return TokenPayloadSchema.from_entity(payload)
