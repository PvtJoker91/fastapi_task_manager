from fastapi import APIRouter, status, Depends, HTTPException

from src.api.filters import PaginationOut, PaginationIn
from src.api.schemas import ApiResponse, ListPaginatedResponse
from src.api.v1.users.schemas import UserSchema, UserCreateSchema
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions import UserAlreadyExists, UserNotFound
from src.apps.users.services import ORMUserService

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/",
             status_code=status.HTTP_201_CREATED, )
async def create_user(
        user_in: UserCreateSchema,
) -> UserSchema:
    try:
        user = await ORMUserService().create_user(user_in=user_in.to_entity())
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"message": e.message})
    user_schema = UserSchema.from_entity(user)
    return user_schema


@router.get("/{username}", response_model=UserSchema)
async def get_user_by_username(
        username: str,
) -> UserSchema:
    try:
        user: UserEntity = await ORMUserService().get_user_by_username(username=username)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": e.message})
    return UserSchema.from_entity(user)


@router.get("/")
async def get_user_list(
        pagination_in: PaginationIn = Depends(),
) -> ApiResponse[ListPaginatedResponse[UserSchema]]:
    user_list = await ORMUserService().get_user_list(pagination=pagination_in)
    items = [UserSchema.from_entity(obj) for obj in user_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )
