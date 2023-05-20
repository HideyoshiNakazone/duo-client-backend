from duo.entity.user_entity import UserEntity
from duo.model.user_model import UserModel

from passlib.hash import pbkdf2_sha256

import unittest


class TestUserModel(unittest.TestCase):
    def test_class_instantiation(self):
        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        self.assertIsInstance(user, UserModel)

    def test_password_hash(self):
        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        self.assertTrue(pbkdf2_sha256.identify(user.password))

    def test_verify_password(self):
        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        self.assertTrue(user.verify_password('password'))

    def test_to_entity(self):
        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        user_entity = user.to_entity()

        self.assertIsInstance(user_entity, UserEntity)

    def test_from_entity(self):
        user_entity = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password',
            _roles='USER'
        )

        user = UserModel.from_entity(user_entity)

        self.assertIsInstance(user, UserModel)

        self.assertIsNone(UserModel.from_entity(None))

    def test_update(self):
        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        expected_user = UserModel(
            username='test',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        user.update(expected_user)

        self.assertEqual(user.username, expected_user.username)
        self.assertEqual(user.fullname, expected_user.fullname)
        self.assertEqual(user.email, expected_user.email)

    def test_to_response(self):
        user = UserModel(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        user = user.to_response()

        self.assertIsNone(user.password)


if __name__ == '__main__':
    unittest.main()
