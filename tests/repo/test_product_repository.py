from duo.repo.product_repository import ProductRepository
from duo.entity.product_entity import Product

from sqlalchemy import create_engine

from unittest import mock
import unittest


class TestProductRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')

    def test_class_instantiation(self):
        repo = ProductRepository(self.engine)

        self.assertIsInstance(repo, ProductRepository)
        self.assertIsNotNone(repo.entity)

    @mock.patch('duo.repo.product_repository.select')
    @mock.patch('duo.repo.product_repository.Session')
    def test_search__product_with_filters(self, session_mock, select_mock):
        repo = ProductRepository(self.engine)

        product1 = Product(
            name='product1',
            description='description1',
            price=1.0
        )
        repo.add(product1)

        product2 = Product(
            name='product2',
            description='description2',
            price=2.0
        )
        repo.add(product2)

        repo.get_product_with_filters('product1', 'description', None)

        select_mock.assert_called_once_with(repo.entity)
        session_mock.assert_called_once_with(repo.engine)

        mock_query = select_mock.return_value
        self.assertEqual(mock_query.order_by.call_count, 1)

        repo.get_product_with_filters('product1', None, 1.0)

        self.assertEqual(mock_query.filter.call_count, 1)
        self.assertEqual(mock_query.order_by.call_count, 1)


if __name__ == '__main__':
    unittest.main()
