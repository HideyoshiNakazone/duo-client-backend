from dotenv import load_dotenv
from functools import cache
import os


@cache
def load_environment_variables() -> dict:
    env_variables = [
        'JWT_SECRET',
        'JWT_ALGORITHM',
        'JWT_EXPIRATION'
    ]
    load_dotenv()

    for env_variable in env_variables:
        if env_variable not in os.environ:
            raise RuntimeError(f"Environment variable {env_variable} not found.")

    return {
        "jwt_secret": os.environ.get('JWT_SECRET'),
        "jwt_algorithm": os.environ.get('JWT_ALGORITHM'),
        "jwt_expiration": os.environ.get('JWT_EXPIRATION'),
    }


def get_jwt_secret():
    return load_environment_variables()['jwt_secret']


def get_jwt_algorithm():
    return load_environment_variables()['jwt_algorithm']


def get_jwt_expiration():
    return load_environment_variables()['jwt_expiration']
