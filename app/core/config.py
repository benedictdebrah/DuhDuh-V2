import os 

from dotenv import load_dotenv

load_dotenv()
import pydantic
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    #project settings
    PROJECT_NAME: str = "Try Out DuhDuh"
    PROJECT_VERSION: str = "0.1.0"

    # #database settings
    # POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tryout")

    #constructed database url
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DATABASE_URL ="sqlite:///database.db"

    #security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    #api settings
    API_V1_STR: str = "/api/v1"


settings = Settings()


