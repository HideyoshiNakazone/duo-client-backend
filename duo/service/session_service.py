from duo.repo.redis_session_repository import RedisSessionRepository
from duo.response.user.user_response import UserResponse

from fastapi import Request, Response
import uuid


class SessionService:

    def __init__(self, session_repo: RedisSessionRepository):
        self.session_repo = session_repo

    def from_request(self, request: Request, response: Response) -> 'SessionService.Session':
        session_id = self._validate_session_id(request.cookies.get('session_id'))
        return self.Session(session_id, self.session_repo, request, response)

    @staticmethod
    def _validate_session_id(session_id: str) -> str:
        if session_id is None:
            return str(uuid.uuid4())
        return session_id

    class Session:
        def __init__(self, session_id: str,
                     session_repo: RedisSessionRepository,
                     request: Request, response: Response):
            self.session_id = session_id
            self.session_repo = session_repo
            self.request = request
            self.response = response

        def store_user_info(self, user_response: UserResponse):
            self.session_repo.add(self.session_id, user_response)
            self.response.set_cookie(
                'session_id',
                self.session_id,
                expires=60 * 60 * 24 * 30,
                httponly=True,
            )

        def get_user_info(self) -> UserResponse:
            return self.session_repo.get(self.session_id)

        def remove_user_info(self):
            self.session_repo.remove(self.session_id)
            self.response.delete_cookie('session_id')
