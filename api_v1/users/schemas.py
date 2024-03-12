from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str
    email: EmailStr | None = None
    active: bool = True


