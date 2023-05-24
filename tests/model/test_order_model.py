from duo.endpoints.order.entity.order_entity import Order
from duo.endpoints.order.model.order_model import OrderModel

from datetime import datetime

import unittest


class TestOrderModel(unittest.TestCase):
    def test_class_instantiation(self):
        order = OrderModel(
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime.now()
        )

        self.assertIsInstance(order, OrderModel)

    def test_to_entity(self):
        order = OrderModel(
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime.now()
        )
        order_entity = order.to_entity()
        self.assertIsInstance(order_entity, Order)

    def test_from_entity(self):
        order_entity = Order(
            id=1,
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime.now()
        )
        order = OrderModel.from_entity(order_entity)
        self.assertIsInstance(order, OrderModel)


if __name__ == '__main__':
    unittest.main()
