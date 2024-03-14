from dataclasses import dataclass
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
