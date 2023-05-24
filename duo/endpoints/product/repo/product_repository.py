from __future__ import annotations

from duo.shared.repository import SQLRepository
from duo.endpoints.product.entity.product_entity import Product

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from sqlalchemy import select


class ProductRepository(SQLRepository):
    entity = Product

    def get_product_with_filters(self, name: str, description: str, price: float, price_range=1, limit=10) -> list[entity] | None:
        query = select(self.entity)

        order_by = []
        if name and isinstance(name, str):
            order_by.append(
                desc(func.similarity(self.entity.name, name))
            )

        if description and isinstance(description, str):
            order_by.append(
                desc(func.similarity(self.entity.description, description))
            )

        if price and isinstance(price, float):
            query = query.filter(
                self.entity.price.between(price - price_range, price + price_range)
            )

        if order_by:
            query = query.order_by(*order_by)

        query = query.limit(limit)

        with Session(self.engine) as session:
            return session.execute(query).scalars().all()
