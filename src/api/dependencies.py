from typing import Annotated

from fastapi import Depends

from src.apps.common.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
