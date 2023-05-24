from duo.endpoints.user.response.token_response import Token
from duo.endpoints.user.model.user_model import UserModel

from dataclasses import dataclass


@dataclass
class UserResponse:
    user: UserModel
    access_token: Token
    refresh_token: Token
    