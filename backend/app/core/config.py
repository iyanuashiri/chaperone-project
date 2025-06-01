from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    SECRET_KEY: str = config('SECRET_KEY')
    DATABASE_URL: PostgresDsn = config('DATABASE_URL')
    
    
settings = Settings()  # type: ignore    