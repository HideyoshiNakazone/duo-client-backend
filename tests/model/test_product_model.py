from duo.entity.product_entity import Product
from duo.model.product_model import ProductModel

import unittest


class TestProductModel(unittest.TestCase):
    def test_class_instantiation(self):
        product_model = ProductModel(
            name='Product Name',
            description='Product Description',
            price=10.0
        )
        self.assertIsInstance(product_model, ProductModel)

    def test_to_entity(self):
        product_model = ProductModel(
            name='Product Name',
            description='Product Description',
            price=10.0
        )
        product_entity = product_model.to_entity()
        self.assertIsInstance(product_entity, Product)

    def test_from_entity(self):
        product_entity = Product(
            name='Product Name',
            description='Product Description',
            price=10.0
        )
        product_model = ProductModel.from_entity(product_entity)
        self.assertIsInstance(product_model, ProductModel)