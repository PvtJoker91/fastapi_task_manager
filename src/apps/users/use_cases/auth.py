from dataclasses import dataclass

from src.apps.users.entities.auth import TokenEntity
from src.apps.users.entities.users import UserEntity
from src.apps.users.services.auth import BaseAuthService, BaseAuthValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class IssueTokenUseCase:
    user_service: BaseUserService
    auth_service: BaseAuthService
    validator_services: list[BaseAuthValidatorService]

    async def execute(self, user_in: UserEntity) -> TokenEntity:
        user = await self.user_service.get_by_username(username=user_in.username)
        token = self.auth_service.issue_token(user=user_in)

        for validator in self.validator_services:
            validator.validate(
                user=user,
                password=user_in.password,
                token=token
            )

        return TokenEntity(
            access_token=token,
            token_type="Bearer",
        )
