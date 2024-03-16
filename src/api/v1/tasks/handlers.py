from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import UOWDep
from src.api.filters import PaginationIn, PaginationOut
from src.api.schemas import ListPaginatedResponse, ApiResponse
from src.api.v1.tasks.filters import TaskFilter
from src.api.v1.tasks.schemas import TaskSchema, TaskCreateSchema
from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.exceptions import TaskNotFound
from src.apps.tasks.services import ORMTaskService
from src.core.db import db_helper

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/count")
async def get_task_count(
        filters: TaskFilter = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = ORMTaskService()
    return await service.get_tasks_count(session=session, filters=filters)


@router.get("/tasks-uow")
async def get_tasks(
        uow: UOWDep,
        pagination_in: PaginationIn = Depends(),
) -> ApiResponse[ListPaginatedResponse[TaskSchema]]:
    tasks = await ORMTaskService().get_tasks(uow, pagination_in)
    items = [TaskSchema.from_entity(obj) for obj in tasks]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        task_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> TaskSchema:
    service = ORMTaskService()
    try:
        task: TaskEntity = await service.get_by_id(session=session, task_id=task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": e.message})
    return TaskSchema.from_entity(task)


@router.get("/")
async def get_task_list(
        pagination_in: PaginationIn = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),

) -> ApiResponse[ListPaginatedResponse[TaskSchema]]:
    service = ORMTaskService()
    task_list = await service.get_task_list(session=session, pagination=pagination_in)
    items = [TaskSchema.from_entity(obj) for obj in task_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
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
