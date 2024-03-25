from dataclasses import dataclass

from src.apps.common.exceptions import ServiceException



@dataclass(eq=False)
class InvalidToken(ServiceException):

    @property
    def message(self):
        return f"Invalid token error"



@dataclass(eq=False)
class IncorrectPassword(ServiceException):

    @property
    def message(self):
        return f"Username or password incorrect"



@dataclass(eq=False)
class UserIsNotActive(ServiceException):
    username: str

    @property
    def message(self):
        return f"User '{self.username}' is not active!"
