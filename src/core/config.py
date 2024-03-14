from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    db_url: str = "postgresql+asyncpg://task_manager_user:qwerty12345@localhost:5432/task_manager"
    # echo: bool = False
    echo: bool = True
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()

    # db_echo: bool = True


settings = Settings()
