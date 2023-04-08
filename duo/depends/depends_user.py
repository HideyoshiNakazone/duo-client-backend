from duo.repo.user_repository import UserRepository
from duo.service.user_service import UserService

from sqlalchemy.engine import Engine, URL
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os


def load_environment_variables() -> dict:
    load_dotenv()

    return {
        "host": os.environ.get('DB_HOST'),
        "port": os.environ.get('DB_PORT'),
        "database": os.environ.get('DB_NAME'),
        "username": os.environ.get('DB_USER'),
        "password": os.environ.get('DB_PASSWORD'),
        "query": None
    }


def get_engine() -> Engine:
    DRIVER = "postgresql+psycopg2"

    url = URL.create(
        DRIVER,
        **load_environment_variables()
    )
    return create_engine(url)


def get_user_repo(engine: Engine) -> UserRepository:
    return UserRepository(engine)


def get_user_service() -> UserService:
    return UserService(get_user_repo(get_engine()))
