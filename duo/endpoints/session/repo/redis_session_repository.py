from duo.endpoints.user.response.user_response import UserResponse
from duo.shared.repository.repository import Repository

import pickle
import redis


class RedisSessionRepository(Repository):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def get(self, session_id: str) -> UserResponse:
        obj = self.redis.get(session_id)
        if obj is None:
            return None
        return pickle.loads(obj)

    def add(self, session_id: str, value: UserResponse) -> None:
        obj = pickle.dumps(value)
        self.redis.set(session_id, obj)

    def remove(self, session_id: str) -> None:
        self.redis.delete(session_id)

    def update(self, session_id: str, value: UserResponse):
        self.add(session_id, value)
