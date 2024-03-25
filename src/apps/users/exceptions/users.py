from dataclasses import dataclass

from src.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class UserNotFound(ServiceException):
    username: str | None = None

    @property
    def message(self):
        return f"User with username '{self.username}' not found"


@dataclass(eq=False)
class UserAlreadyExists(ServiceException):
    username: str

    @property
    def message(self):
        return f"User with username '{self.username}' already exists"
