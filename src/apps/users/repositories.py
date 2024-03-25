from sqlalchemy.orm import DeclarativeBase

from src.apps.common.repositories import SQLAlchemyRepository
from src.apps.users.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
