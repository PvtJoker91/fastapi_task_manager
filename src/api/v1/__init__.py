from fastapi import APIRouter

from .users.handlers import router as users_router
from .auth.handlers import router as auth_router


router = APIRouter(prefix="/v1")
router.include_router(router=users_router)
router.include_router(router=auth_router)
