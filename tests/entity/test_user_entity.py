from duo.entity.user_entity import UserEntity

import unittest


class TestUserEntity(unittest.TestCase):
    def test_class_instantiation(self):
        user = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        self.assertIsInstance(user, UserEntity)

    def test_has_repr(self):
        user = UserEntity(
            username='john_doe',
            fullname='John Doe',
            email='john_doe@email.com',
            password='password'
        )

        expected_repr = "<UserEntity(id=None, username='john_doe', fullname='John Doe', email='john_doe@email.com')>"

        self.assertEqual(user.__repr__(), expected_repr)


if __name__ == '__main__':
    unittest.main()
