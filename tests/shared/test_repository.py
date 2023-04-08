from duo.shared.repository import Repository
from duo.shared.entity import Entity

from sqlalchemy.engine import create_engine
from sqlalchemy import Integer, Column

import unittest


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")

        Entity.metadata.drop_all(self.engine)
        Entity.metadata.clear()

        class Test(Entity):
            __tablename__ = 'test'

            id = Column(Integer, primary_key=True)
            val = Column(Integer, nullable=True)

        self.Test = Test

    def test_class_instantiation(self):
        repository = Repository(self.engine, self.Test)

        self.assertIsInstance(repository, Repository)

    def test_get(self):
        repository = Repository(self.engine, self.Test)

        test_entity = self.Test()
        repository.add(test_entity)

        self.assertEqual(repository.get(1).id, test_entity.id)

    def test_get_all(self):
        repository = Repository(self.engine, self.Test)

        test_entity1 = self.Test(val=1)
        repository.add(test_entity1)

        test_entity2 = self.Test(val=2)
        repository.add(test_entity2)

        self.assertEqual(len(repository.get_all()), 2)

        self.assertEqual(len(repository.get_all(val=1)), 1)

    def test_add(self):
        repository = Repository(self.engine, self.Test)

        test_entity = self.Test()
        repository.add(test_entity)

        self.assertEqual(test_entity.id, 1)

    def test_remove(self):
        repository = Repository(self.engine, self.Test)

        test_entity = self.Test()
        repository.add(test_entity)

        repository.remove(test_entity)

        self.assertEqual(
            repository.get(test_entity.id),
            None
        )

    def test_update(self):
        repository = Repository(self.engine, self.Test)

        test_entity = self.Test(val=1)
        repository.add(test_entity)

        test_entity.val = 2
        repository.update(test_entity)

        self.assertEqual(
            repository.get(test_entity.id).val,
            2
        )


if __name__ == '__main__':
    unittest.main()
