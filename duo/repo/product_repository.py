from __future__ import annotations

from duo.shared.repository import SQLRepository
from duo.entity.product_entity import Product

from sqlalchemy.orm import Session
from sqlalchemy import func


class ProductRepository(SQLRepository):
    entity = Product

    def get_product_by_name(self, name: str, limit=10) -> list[entity] | None:
        with Session(self.engine) as session:
            return session.query(self.entity)\
                .filter(
                    self.entity.name.op("%")(name)
                ).limit(limit).all()

    def get_product_by_description(self, description: str, limit=10) -> list[entity] | None:
        with Session(self.engine) as session:
            return session.query(self.entity)\
                .filter(
                    self.entity.description.op("%")(description)
                ).limit(limit).all()

    def get_product_by_price(self, price: float, price_range=1, limit=10) -> list[entity] | None:
        with Session(self.engine) as session:
            return session.query(self.entity)\
                .filter(
                    self.entity.price.between(price - price_range, price + price_range)
                ).limit(limit).all()
