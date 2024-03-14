from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ListPaginatedResponse, ApiResponse
from src.api.v1.tasks.schemas import TaskSchema, TaskCreateSchema
from src.apps.tasks.services import ORMTaskService
from src.core.db import db_helper

router = APIRouter(tags=["Tasks"])


@router.get("/")
async def get_task_list(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> ApiResponse[ListPaginatedResponse[TaskSchema]]:
    service = ORMTaskService()
    task_list = await service.get_task_list(session=session)
    items = [TaskSchema.from_entity(obj) for obj in task_list]

    return ApiResponse(
        data=ListPaginatedResponse(items=items),
    )


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_in: TaskCreateSchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> TaskSchema:
    service = ORMTaskService()
    task = await service.create(session=session, task_in=task_in.to_entity())
    task_schema = TaskSchema.from_entity(task)

    return task_schema
