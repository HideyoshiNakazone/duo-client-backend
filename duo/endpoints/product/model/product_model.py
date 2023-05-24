from __future__ import annotations

from duo.endpoints.product.entity.product_entity import Product

from dataclasses import dataclass

from typing import Optional


@dataclass
class ProductModel:
    name: str
    description: str
    price: float

    id: Optional[int] = None

    def to_entity(self) -> Product:
        product_entity = Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price
        )
        return product_entity

    def update(self, user_model: ProductModel) -> None:
        self.name = user_model.name
        self.description = user_model.description
        self.price = user_model.price

    @classmethod
    def from_entity(cls, product_entity: Product) -> 'ProductModel' | None:
        if product_entity is None:
            return None
        return cls(
            id=product_entity.id,
            name=product_entity.name,
            description=product_entity.description,
            price=product_entity.price
        )