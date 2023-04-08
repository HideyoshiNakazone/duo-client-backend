from duo.shared.exception.invalid_user_authentication_exception import InvalidUserAuthenticationException
from duo.shared.exception.user_already_exists_exception import UserAlreadyExistsException
from duo.shared.exception.user_not_found_exception import UserNotFoundException
from duo.service.user_service import UserService
from duo.entity.user_entity import UserEntity
from duo.model.user_model import UserModel

from unittest import mock
import unittest


class TestUserService(unittest.TestCase):
    @mock.patch('duo.service.user_service.UserRepository', spec=True)
    def test_class_instantiation(self, mock_user_repo):

        service = UserService(mock_user_repo)

        self.assertIsInstance(service, UserService)

    @mock.patch('duo.service.user_service.UserRepository', spec=True)
    def test_login(self, mock_user_repo):
        service = UserService(mock_user_repo)

        mock_user_repo.get_user_by_username.return_value = None

        with self.assertRaises(UserNotFoundException):
            service.login('john_doe', 'password')

        mock_user_repo.get_user_by_username.return_value = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='error'
        )

        with self.assertRaises(InvalidUserAuthenticationException):
            service.login('john_doe', 'password')

        mock_user_repo.get_user_by_username.return_value = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )
        self.assertEqual(
            service.login('john_doe', 'password').username,
            'john_doe'
        )

    @mock.patch('duo.service.user_service.UserRepository', spec=True)
    def test_register(self, mock_user_repo):
        service = UserService(mock_user_repo)

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
            password='password'
        )
        with self.assertRaises(UserAlreadyExistsException):
            service.register(user)

        mock_user_repo.get_user_by_username.return_value = None
        mock_user_repo.add.return_value = user.to_entity()
        self.assertEqual(
            service.register(user).username,
            'john_doe'
        )


if __name__ == '__main__':
    unittest.main()
