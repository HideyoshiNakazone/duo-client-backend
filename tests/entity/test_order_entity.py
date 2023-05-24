from duo.endpoints.order.entity.order_entity import Order

from datetime import datetime
import unittest


class TestOrderEntity(unittest.TestCase):
    def test_class_instantiation(self):
        order = Order(
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime(2021, 1, 1)
        )

        self.assertIsInstance(order, Order)

    def test_has_repr(self):
        order = Order(
            user_id=1,
            product_id=1,
            quantity=1,
            total_price=1.0,
            delivery_date=datetime(2021, 1, 1)
        )

        expected_repr = '<Order(id=None, user_id=1, product_id=1, quantity=1, total_price=1.0, delivery_date=datetime.datetime(2021, 1, 1, 0, 0))>'

        self.assertEqual(repr(order), expected_repr)


if __name__ == '__main__':
    unittest.main()
