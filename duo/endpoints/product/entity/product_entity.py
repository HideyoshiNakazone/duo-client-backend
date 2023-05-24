from duo.shared.entity import Entity

from sqlalchemy import Column, String, Float, text, Index


class Product(Entity):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    name_idx = Index('name_idx', text("name gin_trgm_ops"), postgresql_using='gin')
    desc_idx = Index('description_idx', text("description gin_trgm_ops"), postgresql_using='gin')
    price_idx = Index('price_idx', text("price gin_trgm_ops"), postgresql_using='gin')

    def __repr__(self):
        return self._repr(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price
        )
