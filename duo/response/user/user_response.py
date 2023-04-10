from duo.response.user.token_response import Token
from duo.model.user_model import UserModel

from dataclasses import dataclass


@dataclass
class UserResponse:
    user: UserModel
    access_token: Token
    refresh_token: Token
    