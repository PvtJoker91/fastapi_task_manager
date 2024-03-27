from typing import Optional

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache


def set_code_cache(email: str, code: str) -> str:
    return code


@cache(namespace="codes")
def get_code_cache(email: str) -> Optional[str]:
    pass


@cache(namespace="codes")
def delete_code_cache(email: str) -> None:
    FastAPICache.clear("codes", email)
