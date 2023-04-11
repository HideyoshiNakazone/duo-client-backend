from duo.service.session_service import SessionService
from duo.response.user.user_response import UserResponse
from duo.response.user.token_response import Token
from duo.model.user_model import UserModel

from datetime import datetime, timedelta
import uuid

from unittest import mock
import unittest


class TestSessionService(unittest.TestCase):
    @mock.patch('duo.service.session_service.RedisSessionRepository', spec=True)
    def test_class_instantiation(self, mock_session_repo):
        service = SessionService(mock_session_repo)
        self.assertIsInstance(service, SessionService)

    @mock.patch('duo.service.session_service.RedisSessionRepository', spec=True)
    def test_from_request(self, mock_session_repo):
        service = SessionService(mock_session_repo)

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
    def setUp(self) -> None:
        self.mock_session_repo = mock.Mock()
        self.mock_request = mock.Mock()
        self.mock_response = mock.Mock()
        self.session = SessionService.Session(
            'session_id',
            self.mock_session_repo,
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


if __name__ == '__main__':
    unittest.main()
