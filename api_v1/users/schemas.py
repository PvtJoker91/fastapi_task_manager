from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str
    email: EmailStr | None = None
    is_active: bool = True


class UserSchema(BaseModel):
    username: str
    email: EmailStr | None = None
    is_active: bool = True
