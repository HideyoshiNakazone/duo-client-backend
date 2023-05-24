from duo.endpoints.order.entity.order_entity import Order
from duo.endpoints.order.repo.order_repository import OrderRepository

from sqlalchemy import create_engine
from datetime import datetime

import unittest


class TestOrderRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')

    def test_class_instantiation(self):
        repo = OrderRepository(self.engine)

        self.assertIsInstance(repo, OrderRepository)

    def test_get_orders_for_user_by_id(self):
        repo = OrderRepository(self.engine)

        repo.add(
            Order(
                user_id=1,
                product_id=1,
                quantity=1,
                total_price=1.0,
                delivery_date=datetime.now()
            )
        )

        orders = repo.get_orders_for_user_by_id(1)

        self.assertEqual(len(orders), 1)


if __name__ == '__main__':
    unittest.main()
