from src.apps.users.repositories import UserRepository
from src.apps.users.services import ORMUserService


def user_service_dependency():
    return ORMUserService(UserRepository)
