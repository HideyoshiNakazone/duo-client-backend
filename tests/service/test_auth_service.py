from duo.service.auth_service import AuthService

from unittest import mock
import unittest


class TestAuthService(unittest.TestCase):
    def test_class_instantiation(self):
        auth_service = AuthService()
        self.assertIsInstance(auth_service, AuthService)

    @mock.patch('duo.service.auth_service.jwt')
    @mock.patch('duo.service.auth_service.get_jwt_expiration')
    def test_generate_auth_token(self,
                                 mock_jwt_expiration,
                                 mock_jwt):

        mock_jwt_expiration.return_value = 3600

        auth_service = AuthService()
        token = auth_service.generate_auth_token(1)

        self.assertTrue(mock_jwt.encode.called)

    @mock.patch('duo.service.auth_service.jwt')
    def test_generate_refresh_token(self, mock_jwt):
        auth_service = AuthService()
        token = auth_service.generate_refresh_token(1)

        self.assertTrue(mock_jwt.encode.called)

    @mock.patch('duo.service.auth_service.get_jwt_secret')
    @mock.patch('duo.service.auth_service.get_jwt_algorithm')
    @mock.patch('duo.service.auth_service.get_jwt_expiration')
    def test_decode_auth_token(self,
                                 mock_jwt_expiration,
                                 mock_jwt_algorithm,
                                 mock_jwt_secret):

        mock_jwt_secret.return_value = 'secret'
        mock_jwt_algorithm.return_value = 'HS256'
        mock_jwt_expiration.return_value = 3600

        authenticated_user_id = 1

        auth_service = AuthService()
        token = auth_service.generate_auth_token(authenticated_user_id)

        user_id = auth_service.decode_auth_token(token)['user_id']

        self.assertEqual(authenticated_user_id, user_id)


if __name__ == '__main__':
    unittest.main()
