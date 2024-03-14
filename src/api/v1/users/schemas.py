from pydantic import BaseModel, EmailStr, ConfigDict

from src.apps.users.entities import UserEntity


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str
    email: EmailStr | None = None
    is_active: bool = True


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    is_active: bool = True

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserSchema':
        return UserSchema(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            is_active=entity.is_active,
        )
