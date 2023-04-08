from duo.entity.user_entity import UserEntity
from duo.model.user_model import UserModel

from passlib.handlers.sha2_crypt import sha256_crypt

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

        self.assertTrue(sha256_crypt.identify(user.password))

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
            password='password'
        )

        user = UserModel.from_entity(user_entity)

        self.assertIsInstance(user, UserModel)

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
