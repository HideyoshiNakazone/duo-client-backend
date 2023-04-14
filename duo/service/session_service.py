from duo.service.auth_service import AuthService
from duo.shared.exception.invalid_user_authentication_exception import InvalidUserAuthenticationException
from duo.repo.redis_session_repository import RedisSessionRepository
from duo.response.user.user_response import UserResponse
from duo.enum.roles_enum import RoleEnum

from fastapi import Request, Response
from datetime import datetime
import uuid


class SessionService:

    def __init__(self,
                 session_repo: RedisSessionRepository,
                 auth_service: AuthService):
        self.session_repo = session_repo
        self.auth_service = auth_service

    def from_request(self, request: Request, response: Response) -> 'SessionService.SessionManager':
        session_id = self._validate_session_id(request.cookies.get('session_id'))
        return self.SessionManager(
            session_id,
            self.session_repo,
            self.auth_service,
            request, response
        )

    @staticmethod
    def _validate_session_id(session_id: str) -> str:
        if session_id is None:
            return str(uuid.uuid4())
        return session_id

    class SessionManager:
        def __init__(self, session_id: str,
                     session_repo: RedisSessionRepository,
                     auth_service: AuthService,
                     request: Request, response: Response):
            self.session_id = session_id

            self.session_repo = session_repo
            self.auth_service = auth_service

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

        def validate_is_logged_in(self):
            if self.get_user_info() is None:
                raise InvalidUserAuthenticationException(
                    "Unauthorized"
                )

        def validate_is_admin(self):
            user_info = self.get_user_info()
            if user_info is None or \
                    user_info.user is None or \
                    RoleEnum.ADMIN not in user_info.user.roles:
                raise InvalidUserAuthenticationException(
                    "Unauthorized"
                )

        def validate_same_user(self, user_id: int):
            user_info = self.get_user_info()
            if user_info is None or \
                    user_info.user is None or \
                    user_info.user.id != user_id:
                raise InvalidUserAuthenticationException(
                    "Unauthorized"
                )

        def refresh_session(self) -> UserResponse:
            user_info = self.get_user_info()

            if user_info is None or user_info.user is None:
                raise InvalidUserAuthenticationException(
                    "Unauthorized"
                )

            if user_info.refresh_token.expiration > datetime.now():
                user_info.access_token = self.auth_service.generate_auth_token(user_info.user.id)

            self.session_repo.update(self.session_id, user_info)

            return user_info
