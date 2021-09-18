from pydantic import BaseSettings

class DotEnvBaseSettings(BaseSettings):
    class Config:
        env_file=".env"
        env_file_encoding = "utf-8"


class CommonSettings(DotEnvBaseSettings):
    APP_NAME: str = "flexi-guitar"
    DEBUG_MODE: bool = False


class ServerSettings(DotEnvBaseSettings):
    HOST: str
    PORT: int


class DatabaseSettings(DotEnvBaseSettings):
    DB_URL: str
    DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()