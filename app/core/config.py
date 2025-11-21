from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    # ALLOWED_ORIGINS: str

    # JWT Configurations

    # SECRET_KEY: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file = ".env"


settings = Settings()
