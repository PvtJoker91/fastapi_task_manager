from dataclasses import dataclass

from src.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class UserNotFound(ServiceException):
    user_id: int | None = None
    username: str | None = None

    @property
    def message(self):
        if self.user_id:
            return f"User with id '{self.user_id}' not found"
        else:
            return f"User with username '{self.username}' not found"


@dataclass(eq=False)
class UserAlreadyExists(ServiceException):
    username: str

    @property
    def message(self):
        return f"User with username '{self.username}' already exists"
