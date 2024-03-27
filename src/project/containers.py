from functools import lru_cache
from logging import (
    getLogger,
    Logger,
)

import punq

from src.apps.common.repositories import AbstractRepository, SQLAlchemyRepository
from src.apps.users.repositories import UserRepository
from src.apps.users.services.auth import (BaseAuthService, BaseAuthValidatorService, ComposedAuthValidatorService,
                                          AuthActiveUserValidatorService, AuthTokenValidatorService,
                                          AuthPasswordValidatorService)
from src.apps.users.services.auth import JWTAuthService
from src.apps.users.services.codes import BaseCodeService, CacheCodeService
from src.apps.users.services.senders import BaseSenderService, EmailSenderService
from src.apps.users.services.users import BaseUserService
from src.apps.users.services.users import ORMUserService
from src.apps.users.use_cases.auth import IssueTokenUseCase
from src.apps.users.use_cases.users import UserRegisterUseCase, UserActivateUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    def build_validators() -> BaseAuthValidatorService:
        return ComposedAuthValidatorService(
            validators=[
                container.resolve(AuthPasswordValidatorService),
                container.resolve(AuthTokenValidatorService),
                container.resolve(AuthActiveUserValidatorService),
            ],
        )

    # init internal stuff
    container.register(Logger, factory=getLogger, name='fastapi.request')

    # init repos
    container.register(AbstractRepository, SQLAlchemyRepository, UserRepository)


    # initialize services
    container.register(BaseAuthService, JWTAuthService)
    container.register(BaseUserService, ORMUserService)
    container.register(BaseCodeService, CacheCodeService)
    container.register(BaseSenderService, EmailSenderService)



    container.register(AuthPasswordValidatorService)
    container.register(AuthTokenValidatorService)
    container.register(AuthActiveUserValidatorService)


    container.register(BaseAuthValidatorService, factory=build_validators)

    # init use cases
    container.register(IssueTokenUseCase)
    container.register(UserRegisterUseCase)
    container.register(UserActivateUseCase)


    return container
