from dataclasses import dataclass

from src.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CodeException(ServiceException):
    @property
    def message(self):
        return 'Auth code exception occurred'


@dataclass(eq=False)
class CodeNotFoundException(CodeException):
    code: str

    @property
    def message(self):
        return 'Code not found'


@dataclass(eq=False)
class CodesNotEqualException(CodeException):
    code: str
    cached_code: str
    user_email: str

    @property
    def message(self):
        return f'Codes are not equal {self.code} {self.cached_code}'
