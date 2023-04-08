from duo.shared.entity import Entity

from sqlalchemy import Integer, Column

import datetime
import re

import unittest


class TestEntity(unittest.TestCase):

    class Test(Entity):
        __tablename__ = 'test'

        id = Column(Integer, primary_key=True)

    def test_class_instantiation(self):

        entity = self.Test()

        self.assertIsInstance(entity, self.Test)

    def test_has_repr(self):

        entity = self.Test()

        expected_repr = "<Test(id=None)>"

        self.assertEqual(entity.__repr__(), expected_repr)

    def test_repr_with_kwargs(self):

        entity = self.Test()

        expected_repr = '<Test(id=1)>'

        self.assertEqual(expected_repr, entity._repr(id=1))

    def test_repr_with_no_kwargs(self):

        entity = self.Test()

        self.assertIsNotNone(re.search(r'<Test [0-9]+>', entity._repr()))


if __name__ == '__main__':
    unittest.main()
