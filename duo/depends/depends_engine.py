from sqlalchemy.engine import Engine, URL
from sqlalchemy import create_engine

from dotenv import load_dotenv
from functools import cache
import os


@cache
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

    url = URL.create(
        DRIVER,
        **load_environment_variables()
    )

    return create_engine(url)
