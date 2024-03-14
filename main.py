from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
