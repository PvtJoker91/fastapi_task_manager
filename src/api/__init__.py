from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from .v1 import router as v1_router



router = APIRouter(prefix="/api")
router.include_router(router=v1_router)
