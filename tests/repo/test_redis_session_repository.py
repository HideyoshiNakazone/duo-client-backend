from duo.endpoints.session.repo.redis_session_repository import RedisSessionRepository
from duo.endpoints.user.response.user_response import UserResponse
from duo.endpoints.user.response.token_response import Token
from duo.endpoints.user.model.user_model import UserModel

from datetime import datetime, timedelta
import pickle

from unittest import mock
import unittest


class TestRedisSessionRepository(unittest.TestCase):
    def setUp(self):

        self.user_data = UserResponse(
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

    @mock.patch('duo.endpoints.session.repo.redis_session_repository.redis')
    def test_class_instantiation(self, mock_redis):
        repo = RedisSessionRepository(mock_redis)

        self.assertIsInstance(repo, RedisSessionRepository)

    @mock.patch('duo.endpoints.session.repo.redis_session_repository.redis')
    def test_get(self, mock_redis):
        repo = RedisSessionRepository(mock_redis)

        mock_redis.get.return_value = pickle.dumps(self.user_data)

        self.assertEqual(self.user_data, repo.get('session_id'))

        mock_redis.get.return_value = None

        self.assertIsNone(repo.get('session_id'))

    @mock.patch('duo.endpoints.session.repo.redis_session_repository.redis')
    def test_add(self, mock_redis):
        repo = RedisSessionRepository(mock_redis)

        repo.add('session_id', self.user_data)

        self.assertTrue(mock_redis.set.called)

    @mock.patch('duo.endpoints.session.repo.redis_session_repository.redis')
    def test_remove(self, mock_redis):
        repo = RedisSessionRepository(mock_redis)

        repo.remove('session_id')

        self.assertTrue(mock_redis.delete.called)

    @mock.patch('duo.endpoints.session.repo.redis_session_repository.redis')
    def test_update(self, mock_redis):
        repo = RedisSessionRepository(mock_redis)

        repo.update('session_id', self.user_data)

        self.assertTrue(mock_redis.set.called)


if __name__ == '__main__':
    unittest.main()
