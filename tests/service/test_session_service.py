from duo.service.auth_service import AuthService
from duo.shared.exception.invalid_user_authentication_exception import InvalidUserAuthenticationException
from duo.service.session_service import SessionService
from duo.response.user.user_response import UserResponse
from duo.response.user.token_response import Token
from duo.model.user_model import UserModel
from duo.enum.roles_enum import RoleEnum

from datetime import datetime, timedelta
from copy import deepcopy
import uuid

from unittest import mock
import unittest


class TestSessionService(unittest.TestCase):
    @mock.patch('duo.service.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.service.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.service.auth_service.get_jwt_expiration', spec=True)
    @mock.patch('duo.service.session_service.RedisSessionRepository', spec=True)
    def test_class_instantiation(self, mock_session_repo,
                                 mock_jwt_expiration,
                                 mock_jwt_algorithm,
                                 mock_jwt_secret):
        mock_jwt_expiration.return_value = 3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        service = SessionService(mock_session_repo, AuthService())
        self.assertIsInstance(service, SessionService)

    @mock.patch('duo.service.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.service.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.service.auth_service.get_jwt_expiration', spec=True)
    @mock.patch('duo.service.session_service.RedisSessionRepository', spec=True)
    def test_from_request(self, mock_session_repo,
                          mock_jwt_expiration,
                          mock_jwt_algorithm,
                          mock_jwt_secret):
        mock_jwt_expiration.return_value = 3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        service = SessionService(mock_session_repo, AuthService())

        mock_request = mock.Mock()
        mock_response = mock.Mock()

        mock_request.cookies.get.return_value = 'session_id'

        session = service.from_request(mock_request, mock_response)

        self.assertEqual(session.session_id, 'session_id')

    def test_validate_session_id(self):
        expected_session_id = 'session_id'
        session_id = SessionService._validate_session_id(expected_session_id)
        self.assertEqual(session_id, 'session_id')

        session_id = SessionService._validate_session_id(None)
        self.assertTrue(self.is_valid_uuid(session_id))

    @staticmethod
    def is_valid_uuid(val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False


class TestSession(unittest.TestCase):

    @mock.patch('duo.service.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.service.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.service.auth_service.get_jwt_expiration', spec=True)
    def setUp(self,
              mock_jwt_expiration,
              mock_jwt_algorithm,
              mock_jwt_secret) -> None:
        mock_jwt_expiration.return_value = 3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        self.mock_session_repo = mock.Mock()
        self.mock_request = mock.Mock()
        self.mock_response = mock.Mock()

        self.session = SessionService.SessionManager(
            'session_id',
            self.mock_session_repo,
            AuthService(),
            self.mock_request,
            self.mock_response,
        )

    def test_store_user_info(self):
        user_data = UserResponse(
            user=UserModel(
                id=1,
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password='password'
            ),
            access_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(minutes=60)
            ),
            refresh_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(days=30)
            ),
        )

        self.session.store_user_info(user_data)

        self.assertTrue(
            self.mock_session_repo.add.called_once_with(
                self.session.session_id,
                user_data
            )
        )
        self.assertTrue(self.mock_response.set_cookie.called)

    def test_get_user_info(self):
        expected_user_data = UserResponse(
            user=UserModel(
                id=1,
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password='password'
            ),
            access_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(minutes=60)
            ),
            refresh_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(days=30)
            ),
        )

        self.mock_session_repo.get.return_value = expected_user_data

        user_data = self.session.get_user_info()

        self.assertEqual(user_data, expected_user_data)

    def test_remove_user_info(self):
        self.session.remove_user_info()

        self.assertTrue(self.mock_session_repo.remove.called_once_with(self.session.session_id))
        self.assertTrue(self.mock_response.delete_cookie.called)

    def test_is_logged_in(self):
        self.mock_session_repo.get.return_value = 'FAKE INFO'
        self.assertFalse(self.session.validate_is_logged_in())

        self.mock_session_repo.get.return_value = None
        with self.assertRaises(InvalidUserAuthenticationException):
            self.session.validate_is_logged_in()

    def test_validate_is_admin(self):
        expected_user_data = UserResponse(
            user=UserModel(
                id=1,
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password='password',
                roles=[RoleEnum.ADMIN]
            ),
            access_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(minutes=60)
            ),
            refresh_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(days=30)
            ),
        )
        self.mock_session_repo.get.return_value = expected_user_data

        self.session.validate_is_admin()

        self.mock_session_repo.get.return_value = None
        with self.assertRaises(InvalidUserAuthenticationException):
            self.session.validate_is_admin()

    def test_validate_same_user(self):
        expected_user_data = UserResponse(
            user=UserModel(
                id=1,
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password='password',
                roles=[RoleEnum.ADMIN]
            ),
            access_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(minutes=60)
            ),
            refresh_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(days=30)
            ),
        )
        self.mock_session_repo.get.return_value = expected_user_data

        self.session.validate_same_user(1)

        with self.assertRaises(InvalidUserAuthenticationException):
            self.session.validate_same_user(2)

    def test_refresh_session(self):
        old_user_info = UserResponse(
            user=UserModel(
                id=1,
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password='password',
                roles=[RoleEnum.ADMIN]
            ),
            access_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(minutes=0)
            ),
            refresh_token=Token(
                token='access_token',
                expiration=datetime.now() + timedelta(days=30)
            ),
        )
        self.mock_session_repo.get.return_value = deepcopy(old_user_info)

        user_info = self.session.refresh_session()

        self.assertTrue(
            old_user_info.access_token.expiration < user_info.access_token.expiration
        )

        self.mock_session_repo.get.return_value = None

        with self.assertRaises(InvalidUserAuthenticationException):
            self.session.refresh_session()


if __name__ == '__main__':
    unittest.main()
