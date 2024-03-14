from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users import services
from src.api.v1.users.schemas import UserSchema, UserCreateSchema
from src.core.db import db_helper

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/",
             status_code=status.HTTP_201_CREATED, )
async def create_user(
        user_in: UserCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await services.create_user(session=session, user_in=user_in)


@router.get("/",
            response_model=list[UserSchema],
            )
async def get_user_list(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await services.get_user_list(session=session)


@router.get("/{username}",
            response_model=UserSchema,)
async def get_user_by_username(
        username: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await services.get_user_by_username(session=session, username=username)
