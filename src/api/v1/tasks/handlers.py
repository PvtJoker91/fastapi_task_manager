from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ListPaginatedResponse, ApiResponse
from src.api.v1.tasks.schemas import TaskSchema
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
