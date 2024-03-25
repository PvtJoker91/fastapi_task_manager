from project.containers import get_container
from src.apps.users.services.auth import JWTAuthService
from src.apps.users.use_cases.auth import IssueTokenUseCase


def token_use_case_dependency():
    container = get_container()
    return container.resolve(IssueTokenUseCase)


def auth_service_dependency():
    return JWTAuthService()
