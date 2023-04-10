from functools import cache

from duo.repo.user_repository import UserRepository
from duo.service.auth_service import AuthService
from duo.service.user_service import UserService

from sqlalchemy.engine import Engine, URL
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os


def load_environment_variables() -> dict:
    env_variables = [
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD'
    ]
    load_dotenv()

    for env_variable in env_variables:
        if env_variable not in os.environ:
            raise RuntimeError(f"Environment variable {env_variable} not found.")

    return {
        "host": os.environ.get('DB_HOST'),
        "port": os.environ.get('DB_PORT'),
        "database": os.environ.get('DB_NAME'),
        "username": os.environ.get('DB_USER'),
        "password": os.environ.get('DB_PASSWORD'),
        "query": None
    }


@cache
def get_engine() -> Engine:
    DRIVER = "postgresql+psycopg2"

    if os.environ.get('ENV') == 'test':
        return create_engine('sqlite:///:memory:')

    url = URL.create(
        DRIVER,
        **load_environment_variables()
    )
    return create_engine(url)


def get_user_repo(engine: Engine) -> UserRepository:
    return UserRepository(engine)


def get_auth_service() -> AuthService:
    return AuthService()


def get_user_service() -> UserService:
    return UserService(
        get_user_repo(get_engine()),
        get_auth_service()
    )
