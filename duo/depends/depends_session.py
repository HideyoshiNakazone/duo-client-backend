from duo.depends.depends_user import get_auth_service
from duo.repo.redis_session_repository import RedisSessionRepository
from duo.service.session_service import SessionService

from dotenv import load_dotenv
from functools import cache
import redis
import os


@cache
def load_environment_variables() -> dict:
    env_variables = [
        'REDIS_HOST',
        'REDIS_PORT',
        'REDIS_PASSWORD',
    ]
    load_dotenv()

    for env_variable in env_variables:
        if env_variable not in os.environ:
            raise RuntimeError(f"Environment variable {env_variable} not found.")

    return {
        "host": os.environ.get('REDIS_HOST'),
        "port": os.environ.get('REDIS_PORT'),
        "password": os.environ.get('REDIS_PASSWORD'),
    }


def get_redis_client() -> redis.Redis:
    return redis.Redis(**load_environment_variables())


def get_redis_session_repo() -> RedisSessionRepository:
    return RedisSessionRepository(get_redis_client())


def get_session_service():
    return SessionService(get_redis_session_repo(), get_auth_service())
