from duo.endpoints.user.repo.user_repository import UserRepository
from duo.endpoints.user.entity.user_entity import UserEntity

from sqlalchemy import create_engine

import unittest


class TestUserRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')

    def test_class_instantiation(self):
        repo = UserRepository(self.engine)

        self.assertIsInstance(repo, UserRepository)
        self.assertIsNotNone(repo.entity)

    def test_get_user_by_username(self):
        repo = UserRepository(self.engine)

        user = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )
        repo.add(user)

        self.assertIsNotNone(
            repo.get_user_by_username('john_doe')
        )

    def test_get_user_by_fullname(self):
        repo = UserRepository(self.engine)

        user = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )
        repo.add(user)

        self.assertIsNotNone(
            repo.get_user_by_fullname('John Doe')
        )

    def test_get_user_by_email(self):
        repo = UserRepository(self.engine)

        user = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )
        repo.add(user)

        self.assertIsNotNone(
            repo.get_user_by_email('john_doe@email.com')
        )


if __name__ == '__main__':
    unittest.main()
