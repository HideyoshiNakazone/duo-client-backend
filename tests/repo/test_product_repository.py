from duo.repo.product_repository import ProductRepository
from duo.entity.product_entity import Product

from sqlalchemy import create_engine

import unittest


class TestProductRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')

    def test_class_instantiation(self):
        repo = ProductRepository(self.engine)

        self.assertIsInstance(repo, ProductRepository)
        self.assertIsNotNone(repo.entity)

    def test_get_product_by_name(self):
        repo = ProductRepository(self.engine)

        product = Product(
            name='Product',
            description='Product description',
            price=100
        )
        repo.add(product)

        self.assertEqual(
            len(repo.get_product_by_name('Product')), 1
        )

    def test_get_product_by_description(self):
        repo = ProductRepository(self.engine)

        product = Product(
            name='Product',
            description='Product description',
            price=100
        )
        repo.add(product)

        self.assertEqual(
            len(repo.get_product_by_description('Product description')), 1
        )

    def test_get_product_by_price(self):
        repo = ProductRepository(self.engine)

        product = Product(
            name='Product',
            description='Product description',
            price=100
        )
        repo.add(product)

        self.assertEqual(
            len(repo.get_product_by_price(100)), 1
        )


if __name__ == '__main__':
    unittest.main()
