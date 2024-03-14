from pydantic import BaseModel


class TaskFilter(BaseModel):
    search: str | None = None
