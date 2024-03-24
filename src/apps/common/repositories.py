from abc import ABC, abstractmethod

from sqlalchemy import insert, update, select, delete, func
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.apps.common.exceptions import ObjNotFoundException, ObjAlreadyExistsException
from src.db.db_helper import db_helper


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, obj_id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    session = db_helper.session_factory()

    async def add_one(self, data: dict):
        async with self.session:
            stmt = insert(self.model).values(**data).returning(self.model)
            try:
                dto = await self.session.execute(stmt)
                await self.session.commit()
                dto = dto.scalar_one()
            except IntegrityError:
                raise ObjAlreadyExistsException
            return dto

    async def edit_one(self, obj_id: int, data: dict):
        async with self.session:
            stmt = update(self.model).values(**data).filter_by(id=obj_id).returning(self.model)
            try:
                dto = await self.session.execute(stmt)
                await self.session.commit()
                dto = dto.scalar_one()
            except NoResultFound:
                raise ObjNotFoundException
            return dto

    async def delete_one(self, obj_id: int):
        async with self.session:
            stmt = delete(self.model).filter_by(id=obj_id)
            await self.session.execute(stmt)
            await self.session.commit()

    async def find_one(self, **filter_by):
        async with self.session:
            stmt = select(self.model).filter_by(**filter_by)
            # res = await self.session.scalar(stmt) # None without exception
            try:
                dto = await self.session.execute(stmt)
                dto = dto.scalar_one()
            except NoResultFound:
                raise ObjNotFoundException
            return dto

    async def find_all(self):
        async with self.session:
            stmt = select(self.model)
            dto_list = await self.session.scalars(stmt)
            return dto_list

    async def count(self) -> int:
        async with self.session:
            query = select(func.count(self.model.id)).select_from(self.model)
            candies_count = await self.session.execute(query)
            await self.session.commit()
            return candies_count.scalar()
