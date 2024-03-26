from src.apps.users.services.auth import JWTAuthService


def auth_service_dependency():
    return JWTAuthService()
