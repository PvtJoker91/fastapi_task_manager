from dataclasses import dataclass, asdict


@dataclass
class TokenEntity:
    access_token: str
    token_type: str


@dataclass
class TokenPayloadEntity:
    sub: str
    email: str | None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items()}
