from duo.depends.depends_auth import get_jwt_secret, get_jwt_algorithm, get_jwt_expiration

from datetime import datetime, timedelta
from dateutil.parser import parse
import jwt


class AuthService:
    JWT_SECRET = get_jwt_secret()
    JWT_ALGORITHM = get_jwt_algorithm()
    JWT_EXPIRATION = get_jwt_expiration()

    def generate_auth_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires": str(datetime.now() + timedelta(seconds=int(self.JWT_EXPIRATION)))
        }
        return jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)

    def generate_refresh_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires": datetime.now() + timedelta(days=30)
        }
        return jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)

    def decode_auth_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return decoded_token if parse(decoded_token["expires"]) >= datetime.now() else None
        except:
            return {}
