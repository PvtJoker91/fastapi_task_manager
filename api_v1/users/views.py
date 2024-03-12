from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud
from api_v1.users.schemas import UserSchema
from core.models import db_helper

router = APIRouter(prefix="/users", )


@router.post("/",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED,)
async def create_user(
    user_in: UserSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)

