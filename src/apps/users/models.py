
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.apps.users.entities import UserEntity
from src.core.db.base import TimedBaseModel


class User(TimedBaseModel):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[bytes]
    is_active: Mapped[bool]
    email: Mapped[str | None]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            is_active=self.is_active,
            email=self.email,
            created_at=self.created_at
        )