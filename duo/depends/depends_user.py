from duo.depends.depends_engine import get_engine
from duo.endpoints.user.repo.user_repository import UserRepository
from duo.auth.auth_service import AuthService
from duo.endpoints.user.service.user_service import UserService

from sqlalchemy.engine import Engine

from dotenv import load_dotenv
from functools import cache
import os


@cache
def load_default_admin_user():
    env_variables = [
        'ADMIN_USERNAME',
        'ADMIN_PASSWORD',
        'ADMIN_EMAIL',
        'ADMIN_FULLNAME'
    ]
    load_dotenv()

    for env_variable in env_variables:
        if env_variable not in os.environ:
            raise RuntimeError(f"Environment variable {env_variable} not found.")

    return {
        "username": os.environ.get('ADMIN_USERNAME'),
        "password": os.environ.get('ADMIN_PASSWORD'),
        "email": os.environ.get('ADMIN_EMAIL'),
        "fullname": os.environ.get('ADMIN_FULLNAME')
    }


def get_user_repo(engine: Engine) -> UserRepository:
    return UserRepository(engine)


def get_auth_service() -> AuthService:
    return AuthService()


def get_user_service() -> UserService:
    return UserService(
        get_user_repo(get_engine()),
        get_auth_service()
    )
