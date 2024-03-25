from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from src.apps.users.entities.users import UserEntity


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


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str

    def to_entity(self):
        return UserEntity(
            username=self.username,
            password=self.password,
        )


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str
    email: EmailStr | None = None

    def to_entity(self):
        return UserEntity(
            username=self.username,
            password=self.password,
            email=self.email,
        )


class UserUpdateSchema(BaseModel):
    username: str
    email: EmailStr | None = None
    is_active: bool

    def to_entity(self):
        return UserEntity(
            username=self.username,
            email=self.email,
            is_active=self.is_active,
            updated_at=datetime.utcnow(),
        )
