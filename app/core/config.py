from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR: Path = Path(__file__).parent.parent.parent


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    threads: int = 4
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_DEFAULT_FORMAT
    log_filename: str


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    name: str
    user: str
    password: str
    host: str
    port: str
    url: str | None = Field(default=None)
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @model_validator(mode="after")
    def set_url(self) -> DatabaseConfig:
        self.url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return self


class RedisConfig(BaseModel):
    host: str
    port: str
    broker_url: str | None = Field(default=None)

    @model_validator(mode="after")
    def set_broker_url(self) -> RedisConfig:
        self.broker_url = f"redis://{self.host}:{self.port}"
        return self


class JWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "app/core/certs/jwt-private.pem"
    public_key_path: Path = BASE_DIR / "app/core/certs/jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(f"{BASE_DIR / '.env.template'}", f"{BASE_DIR / '.env'}"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    debug: bool = False
    allow_origins: list[str]

    logging: LoggingConfig
    db: DatabaseConfig
    redis: RedisConfig

    jwt: JWTConfig = JWTConfig()
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    api: ApiPrefix = ApiPrefix()


settings: Settings = Settings()
