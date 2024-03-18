from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass()
class TaskEntity:
    id: int | None = None
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    assignee_id: int | None = None
    is_visible: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


