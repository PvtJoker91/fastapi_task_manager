import time
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, status, Form, Query
from fastapi.security import OAuth2PasswordBearer
from fastapi_cache.decorator import cache
from orjson import orjson
from punq import Container
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.containers import get_container
from src.api.v1.auth.dependencies import auth_service_dependency
from src.api.v1.auth.schemas import TokenSchema, TokenPayloadSchema, RegisterOutSchema
from src.api.v1.users.schemas import UserCreateSchema
from src.apps.common.exceptions import ServiceException
from src.apps.users.entities.users import UserEntity
from src.apps.users.services.auth import BaseAuthService
from src.apps.users.use_cases.auth import IssueTokenUseCase
from src.apps.users.use_cases.users import UserRegisterUseCase, UserActivateUseCase
from src.db.db_helper import db_helper

router = APIRouter(prefix="/auth", tags=["Auth JWT"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
)


@router.post("/register/", response_model=RegisterOutSchema)
async def register_user(
        user: UserCreateSchema,
        container: Container = Depends(get_container),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    use_case: UserRegisterUseCase = container.resolve(UserRegisterUseCase)
    user_entity: UserEntity = UserEntity(username=user.username, password=user.password, email=user.email)
    try:
        await use_case.execute(user_entity, session)
    except ServiceException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg="User could not register", extra={"error_meta": orjson.dumps(exception).decode()})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return RegisterOutSchema(message=f"Message with account activate instructions has sent to email '{user.email}'")


@router.post("/activate/")
async def activate_account(
        code: str = Query(),
        username: str = Query(),
        container: Container = Depends(get_container),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    use_case: UserActivateUseCase = container.resolve(UserActivateUseCase)
    try:
        token = await use_case.execute(code=code, username=username, session=session)
    except ServiceException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg="User activation problem", extra={"error_meta": orjson.dumps(exception).decode()})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return TokenSchema.from_entity(token)


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
        )

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


@router.get("/cached_data/")
@cache(expire=10, namespace="bbb")
def get_data():
    time.sleep(1)
    return "Very big data set"
