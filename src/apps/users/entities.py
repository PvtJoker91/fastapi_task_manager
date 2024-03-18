from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass()
class UserEntity:
    id: int | None = None
    username: str | None = None
    is_active: bool = True
    email: str | None = None
    password: str | bytes | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}
