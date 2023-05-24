from duo.shared.exception.invalid_resource_exception import InvalidResourceException
from duo.endpoints.user.response.token_response import Token
from duo.auth.auth_service import AuthService

from datetime import datetime
from unittest import mock
import unittest


class TestAuthService(unittest.TestCase):
    @mock.patch('duo.auth.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_expiration', spec=True)
    def test_class_instantiation(self,
                                 mock_jwt_expiration,
                                 mock_jwt_algorithm,
                                 mock_jwt_secret):
        auth_service = AuthService()
        self.assertIsInstance(auth_service, AuthService)

    @mock.patch('duo.auth.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_expiration', spec=True)
    def test_generate_auth_token(self,
                                 mock_jwt_expiration,
                                 mock_jwt_algorithm,
                                 mock_jwt_secret):
        mock_jwt_expiration.return_value = 3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        auth_service = AuthService()
        token = auth_service.generate_auth_token(1)

        self.assertIsInstance(token, Token)

        self.assertIsInstance(token.token, str)
        self.assertIsInstance(token.expiration, datetime)

    @mock.patch('duo.auth.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_expiration', spec=True)
    def test_generate_refresh_token(self,
                                    mock_jwt_expiration,
                                    mock_jwt_algorithm,
                                    mock_jwt_secret):
        mock_jwt_expiration.return_value = 3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        auth_service = AuthService()
        token = auth_service.generate_refresh_token(1)

        self.assertIsInstance(token, Token)

        self.assertIsInstance(token.token, str)
        self.assertIsInstance(token.expiration, datetime)

    @mock.patch('duo.auth.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_expiration', spec=True)
    def test_decode_auth_token_when_valid(self,
                               mock_jwt_expiration,
                               mock_jwt_algorithm,
                               mock_jwt_secret):
        mock_jwt_expiration.return_value = 3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        authenticated_user_id = 1

        auth_service = AuthService()
        token = auth_service.generate_auth_token(authenticated_user_id)


        user_id = auth_service.decode_auth_token(token)['user_id']

        self.assertEqual(authenticated_user_id, user_id)

    @mock.patch('duo.auth.auth_service.get_jwt_secret', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_algorithm', spec=True)
    @mock.patch('duo.auth.auth_service.get_jwt_expiration', spec=True)
    def test_decode_auth_token_when_invalid(self,
                               mock_jwt_expiration,
                               mock_jwt_algorithm,
                               mock_jwt_secret):
        mock_jwt_expiration.return_value = -3600
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_secret.return_value = 'secret'

        authenticated_user_id = 1

        auth_service = AuthService()
        token = auth_service.generate_auth_token(authenticated_user_id)

        with self.assertRaises(InvalidResourceException):
            auth_service.decode_auth_token(token)['user_id']


if __name__ == '__main__':
    unittest.main()
