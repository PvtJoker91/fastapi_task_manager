from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass()
class UserEntity:
    id: int | None = field(default=None, kw_only=True)  # noqa
    username: str
    is_active: bool
    email: str
    password: str | bytes | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items()}
