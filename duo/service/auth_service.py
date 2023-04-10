from duo.depends.depends_auth import get_jwt_secret, get_jwt_algorithm, get_jwt_expiration
from duo.shared.exception.invalid_resource_exception import InvalidResourceException
from duo.response.user.token_response import Token

from datetime import datetime, timedelta
from dateutil.parser import parse
import jwt


class AuthService:
    JWT_SECRET = get_jwt_secret()
    JWT_ALGORITHM = get_jwt_algorithm()
    JWT_EXPIRATION = get_jwt_expiration()

    def generate_auth_token(self, user_id: int) -> Token:
        expiration_date = datetime.now() + timedelta(seconds=int(self.JWT_EXPIRATION))
        payload = {
            "user_id": user_id,
            "expires": str(expiration_date)
        }
        return Token(
            token=jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM),
            expiration=expiration_date
        )

    def generate_refresh_token(self, user_id: int) -> Token:
        expiration_date = datetime.now() + timedelta(days=30)
        payload = {
            "user_id": user_id,
            "expires": str(expiration_date)
        }
        return Token(
            token=jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM),
            expiration=expiration_date
        )

    def decode_auth_token(self, token: Token) -> dict:
        decoded_token = jwt.decode(token.token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
        if parse(decoded_token["expires"]) >= datetime.now():
            return decoded_token

        raise InvalidResourceException("Token has expired")
