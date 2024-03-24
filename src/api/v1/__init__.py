from fastapi import APIRouter

from .users.routers import router as users_router
from .auth.routers import router as auth_router
from .tasks.routers import router as tasks_router


router = APIRouter(prefix="/v1")
router.include_router(router=users_router)
router.include_router(router=auth_router)
router.include_router(router=tasks_router)
