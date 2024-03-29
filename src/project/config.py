from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseSettings):
    mode: str
    echo: bool = False
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class RedisSettings(BaseSettings):
    cache_url: str
    broker_url: str
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    redis: RedisSettings = RedisSettings()


settings = Settings()
