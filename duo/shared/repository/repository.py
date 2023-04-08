from duo.shared.entity import Entity

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import datetime


class Repository:
    __slots__ = ['engine', 'entity', 'metadata']

    entity: Entity

    def __init__(self, engine: Engine, entity: Entity = None):
        self.engine = engine

        if entity is not None:
            self.entity = entity

        self.entity.metadata.create_all(self.engine)
        self.metadata = self.entity.__table__

    def get(self, id: int) -> Entity:
        with Session(self.engine) as session:
            return session.get(self.entity, id)

    def get_all(self, **kwargs) -> list[Entity]:
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

    def add(self, entity: Entity) -> Entity:
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(entity)

            session.commit()

        return entity

    def remove(self, entity: Entity) -> None:
        with Session(self.engine) as session:
            session.delete(entity)

            session.commit()

    def update(self, entity: Entity) -> Entity:
        entity.modified_at = datetime.datetime.utcnow()
        with Session(self.engine, expire_on_commit=False) as session:
            session.merge(entity)

            session.commit()

        return entity
