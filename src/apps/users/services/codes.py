from abc import ABC, abstractmethod
from random import randint

from src.apps.users.entities.users import UserEntity
from src.apps.users.exceptions.codes import CodeNotFoundException, CodesNotEqualException
from src.apps.users.utils import codes as code_utils


class BaseCodeService(ABC):

    @abstractmethod
    def generate_code(self, user: UserEntity) -> str:
        ...

    @abstractmethod
    def validate_code(self, code: str, user: UserEntity) -> None:
        ...


class CacheCodeService(BaseCodeService):
    def generate_code(self, user: UserEntity) -> str:
        code = str(randint(100000, 999999))
        code_utils.set_code_cache(email=user.email, code=code)
        return code

    def validate_code(self, code: str, user: UserEntity):
        cached_code = code_utils.get_code_cache(email=user.email)

        if cached_code is None:
            raise CodeNotFoundException(code=code)

        if cached_code != code:
            raise CodesNotEqualException(
                code=code,
                cached_code=cached_code,
                user_email=user.email,
            )
        code_utils.delete_code_cache(user.email)
