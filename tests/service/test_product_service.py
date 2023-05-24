from duo.shared.exception.resource_not_found import ResourceNotFoundException
from duo.endpoints.product.service.product_service import ProductService
from duo.endpoints.product.model.product_model import ProductModel
from duo.endpoints.product.entity.product_entity import Product

from unittest import mock
import unittest


class TestProductService(unittest.TestCase):
    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_class_instantiation(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        self.assertIsInstance(product_service, ProductService)

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_get_products(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        mock_product_repo.get_all.return_value = [
            Product(
                id=1,
                name='test',
                description='test',
                price=1.0
            ),
            Product(
                id=2,
                name='test',
                description='test',
                price=1.0
            )
        ]

        products = product_service.get_products()

        self.assertEqual(len(products), 2)

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_get_product(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        mock_product_repo.get.return_value = Product(
            id=1,
            name='test',
            description='test',
            price=1.0
        )

        product = product_service.get_product(1)

        self.assertEqual(product.id, 1)

        mock_product_repo.get.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            product_service.get_product(1)

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_add_product(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        expected_product = Product(
            id=1,
            name='test',
            description='test',
            price=1.0
        )

        mock_product_repo.add.return_value = expected_product

        product = product_service.add_product(
            ProductModel.from_entity(expected_product)
        )

        self.assertEqual(product.id, 1)

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_update_product(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        expected_product = Product(
            id=1,
            name='test',
            description='test',
            price=1.0
        )

        mock_product_repo.get.return_value = expected_product
        mock_product_repo.update.return_value = expected_product

        product = product_service.update_product(
            1,
            ProductModel.from_entity(expected_product)
        )

        self.assertEqual(product.id, 1)

        mock_product_repo.get.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            product_service.update_product(
                1,
                ProductModel.from_entity(expected_product)
            )

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_remove_product(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        mock_product_repo.get.return_value = Product(
            id=1,
            name='test',
            description='test',
            price=1.0
        )

        product_service.remove_product(1)

        mock_product_repo.get.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            product_service.remove_product(1)

    @mock.patch('duo.auth.auth_service.AuthService', spec=True)
    @mock.patch('duo.endpoints.product.repo.product_repository.ProductRepository', spec=True)
    def test_search_products(self, mock_product_repo, mock_auth_service):
        product_service = ProductService(
            mock_product_repo,
            mock_auth_service
        )

        mock_product_repo.get_product_with_filters.return_value = [
            Product(
                id=1,
                name='test',
                description='test',
                price=1.0
            ),
            Product(
                id=2,
                name='test',
                description='test',
                price=1.0
            )
        ]

        products = product_service.search_products(name='test')

        self.assertEqual(len(products), 2)


if __name__ == '__main__':
    unittest.main()
