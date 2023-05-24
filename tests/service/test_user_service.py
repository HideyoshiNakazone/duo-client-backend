from duo.shared.exception.invalid_user_authentication_exception import InvalidUserAuthenticationException
from duo.shared.exception.user_already_exists_exception import UserAlreadyExistsException
from duo.shared.exception.user_not_found_exception import UserNotFoundException
from duo.endpoints.user.service.user_service import UserService
from duo.endpoints.user.entity.user_entity import UserEntity
from duo.endpoints.user.model.user_model import UserModel

from unittest import mock
import unittest


class TestUserService(unittest.TestCase):
    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.user.service.user_service.UserRepository', spec=True)
    def test_class_instantiation(self, mock_user_repo, mock_auth_service):
        service = UserService(mock_user_repo, mock_auth_service)

        self.assertIsInstance(service, UserService)

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.user.service.user_service.UserRepository', spec=True)
    def test_get_users(self, mock_user_repo, mock_auth_service):
        service = UserService(mock_user_repo, mock_auth_service)

        mock_user_repo.get_all.return_value = [
            UserEntity(
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password='passwd',
                _roles='USER'
            ),
            UserEntity(
                username='maria_doe',
                fullname='Maria Doe',
                email='maria_doe@email.com',
                password='passwd',
                _roles='USER'
            )
        ]

        expected_users = [
            UserModel(
                username='john_doe',
                fullname='John Doe',
                email='john_doe@email.com',
                password=None
            ),
            UserModel(
                username='maria_doe',
                fullname='Maria Doe',
                email='maria_doe@email.com',
                password=None
            )
        ]

        self.assertEqual(expected_users, service.get_users())

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.user.service.user_service.UserRepository', spec=True)
    def test_login(self, mock_user_repo, mock_auth_service):
        service = UserService(mock_user_repo, mock_auth_service)

        mock_user_repo.get_user_by_username.return_value = None

        with self.assertRaises(UserNotFoundException):
            service.login('john_doe', 'password')

        mock_user_repo.get_user_by_username.return_value = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='error',
            _roles='USER'
        )

        with self.assertRaises(InvalidUserAuthenticationException):
            service.login('john_doe', 'password')

        mock_user_repo.get_user_by_username.return_value = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password',
            _roles='USER'
        )
        self.assertEqual(
            service.login('john_doe', 'password').user.username,
            'john_doe'
        )

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.user.service.user_service.UserRepository', spec=True)
    def test_register(self, mock_user_repo, mock_auth_service):
        service = UserService(mock_user_repo, mock_auth_service)

        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        mock_user_repo.get_user_by_username.return_value = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password',
            _roles='USER'
        )
        with self.assertRaises(UserAlreadyExistsException):
            service.register(user)

        mock_user_repo.get_user_by_username.return_value = None
        mock_user_repo.add.return_value = user.to_entity()
        self.assertEqual(
            service.register(user).user.username,
            'john_doe'
        )

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.user.service.user_service.UserRepository', spec=True)
    def test_remove(self, mock_user_repo, mock_auth_service):
        service = UserService(mock_user_repo, mock_auth_service)

        mock_user_repo.get.return_value = None
        with self.assertRaises(UserNotFoundException):
            service.remove(1)

        mock_user_repo.get.return_value = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password',
            _roles='USER'
        )
        self.assertIsNone(service.remove(1))

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.user.service.user_service.UserRepository', spec=True)
    def test_update(self, mock_user_repo, mock_auth_service):
        service = UserService(mock_user_repo, mock_auth_service)

        user = UserEntity(
            id=1,
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password',
            _roles='USER'
        )

        expected_entity = UserModel(
            id=1,
            username='test',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        mock_user_repo.get.return_value = None
        with self.assertRaises(UserNotFoundException):
            service.update(1, expected_entity)

        mock_user_repo.get.return_value = user
        mock_user_repo.update.return_value = expected_entity

        updated_user = service.update(1, expected_entity)

        self.assertEqual(expected_entity.id, updated_user.id)
        self.assertEqual(expected_entity.username, updated_user.username)
        self.assertEqual(expected_entity.fullname, updated_user.fullname)
        self.assertEqual(expected_entity.email, updated_user.email)


if __name__ == '__main__':
    unittest.main()
