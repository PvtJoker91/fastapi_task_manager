import time
from contextlib import asynccontextmanager

from celery import Celery
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.project.config import settings
from src.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.redis.cache_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan,)
app.include_router(router=api_router)


celery = Celery(
    "celery",
    broker=settings.redis.broker_url,
    backend=settings.redis.broker_url,
)


@celery.task()
def test_task():
    time.sleep(10)
    print("task complete")


@app.get("/test")
def test():
    test_task.delay()
