from datetime import datetime

from duo.endpoints.order.entity.order_entity import Order
from duo.endpoints.order.model.order_model import OrderModel
from duo.endpoints.order.service.order_service import OrderService

from unittest import mock
import unittest

from duo.endpoints.product.entity.product_entity import Product
from duo.shared.exception.invalid_resource_exception import InvalidResourceException


class TestOrderService(unittest.TestCase):
    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_class_instantiation(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        self.assertIsInstance(order_service, OrderService)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_get_orders(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        mock_order_repo.get_all.return_value = [
            Order(
                id=1,
                user_id=1,
                product_id=1,
                quantity=1,
                total_price=1.0,
                delivery_date=datetime.now()
            ),
            Order(
                id=2,
                user_id=1,
                product_id=1,
                quantity=1,
                total_price=1.0,
                delivery_date=datetime.now()
            )
        ]

        orders = order_service.get_orders()

        self.assertEqual(len(orders), 2)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_get_order(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        mock_order_repo.get.return_value = Order(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime.now()
        )

        order = order_service.get_order(1)

        self.assertIsInstance(order, Order)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_get_orders_for_user_by_id(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        mock_order_repo.get_orders_for_user_by_id.return_value = [
            Order(
                id=1,
                user_id=1,
                product_id=1,
                quantity=1,
                total_price=1.0,
                delivery_date=datetime.now()
            ),
            Order(
                id=2,
                user_id=1,
                product_id=1,
                quantity=1,
                total_price=1.0,
                delivery_date=datetime.now()
            )
        ]

        orders = order_service.get_orders_for_user_by_id(1)

        self.assertEqual(len(orders), 2)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_add_order(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        expected_order = OrderModel(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime(2021, 1, 1)
        )

        mock_order_repo.add.return_value = expected_order.to_entity()

        mock_product_repo.get.return_value = Product(
            id=1,
            name='Test Product',
            description='Test Description',
            price=1.0,
        )

        order = order_service.add_order(
            OrderModel(
                id=1,
                user_id=1,
                product_id=1,
                quantity=1,
                delivery_date=datetime(2021, 1, 1)
            )
        )

        self.assertEqual(order, expected_order)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_add_order_with_invalid_product_id(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        mock_product_repo.get.return_value = None

        with self.assertRaises(InvalidResourceException):
            order_service.add_order(
                OrderModel(
                    id=1,
                    user_id=1,
                    product_id=1,
                    quantity=1,
                    delivery_date=datetime(2021, 1, 1)
                )
            )

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_update_order(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        expected_order = OrderModel(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=0.0,
            delivery_date=datetime(2021, 1, 1)
        )

        mock_order_repo.get.return_value = expected_order.to_entity()

        expected_order.total_price = 1.0

        mock_order_repo.update.return_value = expected_order.to_entity()

        mock_product_repo.get.return_value = Product(
            id=1,
            name='Test Product',
            description='Test Description',
            price=1.0,
        )

        order = order_service.update_order(
            OrderModel(
                id=1,
                user_id=1,
                product_id=1,
                quantity=1,
                delivery_date=datetime(2021, 1, 1)
            )
        )

        self.assertEqual(order, expected_order)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_update_order_with_invalid_order(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        expected_order = OrderModel(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=0.0,
            delivery_date=datetime(2021, 1, 1)
        )

        mock_order_repo.get.return_value = None

        with self.assertRaises(InvalidResourceException):
            order_service.update_order(
                OrderModel(
                    id=1,
                    user_id=1,
                    product_id=1,
                    quantity=1,
                    delivery_date=datetime(2021, 1, 1)
                )
            )

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_update_order_with_invalid_product(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        expected_order = OrderModel(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=0.0,
            delivery_date=datetime(2021, 1, 1)
        )

        mock_order_repo.get.return_value = expected_order.to_entity()

        expected_order.total_price = 1.0

        mock_order_repo.update.return_value = expected_order.to_entity()

        mock_product_repo.get.return_value = None

        with self.assertRaises(InvalidResourceException):
            order_service.update_order(
                OrderModel(
                    id=1,
                    user_id=1,
                    product_id=1,
                    quantity=1,
                    delivery_date=datetime(2021, 1, 1)
                )
            )

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_delete_order(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        mock_order_repo.get.return_value = Order(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=0.0,
            delivery_date=datetime(2021, 1, 1)
        )

        mock_order_repo.delete.return_value = True

        order_service.delete_order(1)

    @mock.patch('duo.endpoints.order.service.order_service.OrderRepository')
    @mock.patch('duo.endpoints.product.service.product_service.ProductRepository')
    def test_delete_raises_exception(self, mock_order_repo, mock_product_repo):
        order_service = OrderService(mock_order_repo, mock_product_repo)

        mock_order_repo.get.return_value = None

        with self.assertRaises(InvalidResourceException):
            order_service.delete_order(1)
