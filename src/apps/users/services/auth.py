from abc import ABC, abstractmethod
from dataclasses import dataclass

from jwt import InvalidTokenError

from src.apps.users.entities.auth import TokenPayloadEntity
from src.apps.users.entities.users import UserEntity
from src.apps.users.exceptions.auth import IncorrectPassword, UserIsNotActive, InvalidToken
from src.apps.users.utils import auth as auth_utils


class BaseAuthService(ABC):
    @abstractmethod
    def issue_token(self, user: UserEntity):
        ...

    def get_user_from_token(self, token: str) -> TokenPayloadEntity:
        ...


class JWTAuthService(BaseAuthService):

    def issue_token(self, user: UserEntity) -> str:
        jwt_payload = TokenPayloadEntity(
            sub=user.username,
            email=user.email,
        )
        token = auth_utils.encode_jwt(jwt_payload)
        return token

    def get_user_from_token(self, token: str) -> TokenPayloadEntity:
        try:
            payload = auth_utils.decode_jwt(token=token)
        except InvalidTokenError:
            raise InvalidToken
        if not (username := payload["sub"]):
            raise InvalidToken
        return TokenPayloadEntity(
            sub=username,
            email=payload["email"]
        )


class BaseAuthValidatorService(ABC):
    @abstractmethod
    def validate(self, *args, **kwargs):
        ...


class AuthTokenValidatorService(BaseAuthValidatorService):

    def validate(self, user: UserEntity, token: str, **kwargs):
        ...


class AuthPasswordValidatorService(BaseAuthValidatorService):

    def validate(self, user: UserEntity, password: str, **kwargs):
        if not auth_utils.validate_password(
                password=password,
                hashed_password=user.password,
        ):
            raise IncorrectPassword()


class AuthActiveUserValidatorService(BaseAuthValidatorService):

    def validate(self, user: UserEntity, **kwargs):
        if not user.is_active:
            raise UserIsNotActive(username=user.username)


@dataclass
class ComposedAuthValidatorService(BaseAuthValidatorService):
    validators: list[BaseAuthValidatorService]

    def validate(
            self,
            user: UserEntity,
            password: bytes | None = None,
            token: str | None = None,
    ):
        for validator in self.validators:
            validator.validate(user=user, password=password, token=token)
