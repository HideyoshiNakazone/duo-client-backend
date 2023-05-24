from duo.endpoints.product.entity.product_entity import Product

import unittest


class TestProductEntity(unittest.TestCase):
    def test_class_instantiation(self):
        product = Product(
            name='name',
            description='description',
            price=1.0
        )

        self.assertIsInstance(product, Product)

    def test_has_repr(self):
        product = Product(
            name='name',
            description='description',
            price=1.0
        )
        expected = "<Product(id=None, name='name', description='description', price=1.0)>"
        
        self.assertEqual(expected, repr(product))


if __name__ == '__main__':
    unittest.main()
