
from dataclasses import dataclass
from datetime import datetime


@dataclass()
class UserEntity:
    id: int  # noqa
    username: str
    is_active: bool
    email: str
    created_at: datetime
