from duo.shared.repository.repository import Repository
from duo.shared.entity import Entity

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import datetime


class SQLRepository(Repository):
    entity = Entity

    def __init__(self, engine: Engine, entity: Entity = None):
        self.engine = engine

        if entity is not None:
            self.entity = entity

        self.entity.metadata.create_all(self.engine)
        self.metadata = self.entity.__table__

    def get(self, id: int) -> entity:
        with Session(self.engine) as session:
            return session.get(self.entity, id)

    def get_all(self, **kwargs) -> list[entity]:
        with Session(self.engine) as session:
            query = session.query(self.entity)

            query_params = {}
            for key, value in kwargs.items():
                if key in [c.name for c in self.metadata.columns]:
                    if value is not None:
                        query_params[key] = value
            if query_params:
                query = query.filter_by(**query_params)

        return query.all()

    def add(self, entity: entity) -> entity:
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(entity)

            session.commit()

        return entity

    def remove(self, entity: entity) -> None:
        with Session(self.engine) as session:
            session.delete(entity)

            session.commit()

    def update(self, entity: entity) -> entity:
        entity.modified_at = datetime.datetime.utcnow()
        with Session(self.engine, expire_on_commit=False) as session:
            session.merge(entity)

            session.commit()

        return entity
