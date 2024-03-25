from pydantic import BaseModel

from src.apps.users.entities.auth import TokenEntity, TokenPayloadEntity


class TokenPayloadSchema(BaseModel):
    sub: str
    email: str | None

    @staticmethod
    def from_entity(entity: TokenPayloadEntity) -> 'TokenPayloadSchema':
        return TokenPayloadSchema(
            sub=entity.sub,
            email=entity.email
        )


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    @staticmethod
    def from_entity(entity: TokenEntity) -> 'TokenSchema':
        return TokenSchema(
            access_token=entity.access_token,
            token_type=entity.token_type
        )
