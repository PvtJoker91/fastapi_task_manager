from dataclasses import dataclass, asdict
from datetime import datetime

from src.apps.users.entities import UserEntity


@dataclass()
class TaskEntity:
    id: int  # noqa
    title: str
    description: str
    is_visible: bool
    user: UserEntity
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}
