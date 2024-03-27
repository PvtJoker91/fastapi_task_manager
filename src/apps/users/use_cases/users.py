from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.entities.auth import TokenEntity
from src.apps.users.entities.users import UserEntity
from src.apps.users.services.auth import BaseAuthService
from src.apps.users.services.codes import BaseCodeService
from src.apps.users.services.senders import BaseSenderService
from src.apps.users.services.users import BaseUserService


@dataclass
class UserRegisterUseCase:
    user_service: BaseUserService
    sender_service: BaseSenderService

    async def execute(self, user_in: UserEntity, session: AsyncSession):
        user = await self.user_service.create_user(user_in=user_in, session=session)
        message = f""
        return self.sender_service.send_message(user, message)


@dataclass
class UserActivateUseCase:
    user_service: BaseUserService
    code_service: BaseCodeService
    auth_service: BaseAuthService

    async def execute(self, code: str, username: str, session: AsyncSession) -> TokenEntity:
        user = await self.user_service.get_by_username(username=username, session=session)
        self.code_service.validate_code(code=code, user=user)
        user.is_active = True
        await self.user_service.update_user(user_in=user, user_id=user.id, session=session)
        token = self.auth_service.issue_token(user=user)
        return TokenEntity(
            access_token=token,
            token_type="Bearer",
        )

