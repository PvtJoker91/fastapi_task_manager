
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import insert, update, select, delete, func
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.apps.common.exceptions import ObjNotFoundException, ObjAlreadyExistsException
from src.db.db_helper import db_helper


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, data: dict, session: AsyncSession):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, obj_id: int, data: dict, session: AsyncSession):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, obj_id: int, session: AsyncSession):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, session: AsyncSession):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, session: AsyncSession):
        raise NotImplementedError

    @abstractmethod
    async def count(self, session: AsyncSession):
        raise NotImplementedError


@dataclass
class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict, session: AsyncSession):
        stmt = insert(self.model).values(**data).returning(self.model)
        try:
            dto = await session.execute(stmt)
            await session.commit()
            dto = dto.scalar_one()
        except IntegrityError:
            raise ObjAlreadyExistsException
        return dto

    async def edit_one(self, obj_id: int, data: dict, session: AsyncSession):
        stmt = update(self.model).values(**data).filter_by(id=obj_id).returning(self.model)
        try:
            dto = await session.execute(stmt)
            await session.commit()
            dto = dto.scalar_one()
        except NoResultFound:
            raise ObjNotFoundException
        return dto

    async def delete_one(self, obj_id: int, session: AsyncSession):
        stmt = delete(self.model).filter_by(id=obj_id)
        await session.execute(stmt)
        await session.commit()

    async def find_one(self, session: AsyncSession, **filter_by):
        # async with self.session:
        stmt = select(self.model).filter_by(**filter_by)
        # res = await self.session.scalar(stmt) # None without exception
        try:
            dto = await session.execute(stmt)
            dto = dto.scalar_one()
        except NoResultFound:
            raise ObjNotFoundException
        return dto

    async def find_all(self, session: AsyncSession):
        stmt = select(self.model)
        dto_list = await session.scalars(stmt)
        return dto_list

    async def count(self, session: AsyncSession) -> int:
        query = select(func.count(self.model.id)).select_from(self.model)
        candies_count = await session.execute(query)
        await session.commit()
        return candies_count.scalar()
