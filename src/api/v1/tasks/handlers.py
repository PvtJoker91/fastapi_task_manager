from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import UOWDep
from src.api.filters import PaginationIn, PaginationOut
from src.api.schemas import ListPaginatedResponse, ApiResponse
from src.api.v1.tasks.filters import TaskFilter
from src.api.v1.tasks.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from src.apps.tasks.entities import TaskEntity
from src.apps.tasks.exceptions import TaskNotFound
from src.apps.tasks.services import ORMTaskService
from src.core.db import db_helper

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
        uow: UOWDep,
        task_in: TaskCreateSchema,
) -> TaskSchema:
    task = await ORMTaskService().create_task(uow, task_in=task_in.to_entity())
    task_schema = TaskSchema.from_entity(task)
    return task_schema


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
        uow: UOWDep,
        task_id: int,
        task_in: TaskUpdateSchema,
) -> TaskSchema:
    try:
        task = await ORMTaskService().update_task(uow, task_id=task_id, task_in=task_in.to_entity())
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": e.message})
    return TaskSchema.from_entity(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        uow: UOWDep,
        task_id: int,
) -> None:
    try:
        await ORMTaskService().delete_task(uow, task_id=task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": e.message})


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        uow: UOWDep,
        task_id: int,
) -> TaskSchema:
    try:
        task: TaskEntity = await ORMTaskService().get_task_by_id(uow, task_id=task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": e.message})
    return TaskSchema.from_entity(task)


@router.get("/")
async def get_task_list(
        uow: UOWDep,
        pagination_in: PaginationIn = Depends(),
) -> ApiResponse[ListPaginatedResponse[TaskSchema]]:
    tasks = await ORMTaskService().get_task_list(uow, pagination_in)
    items = [TaskSchema.from_entity(obj) for obj in tasks]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )
