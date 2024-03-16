from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass()
class TaskEntity:
    id: int | None = field(default=None, kw_only=True)  # noqa
    title: str
    description: str
    author_id: int
    assignee_id: int
    is_visible: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items()}
