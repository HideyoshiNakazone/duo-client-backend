from __future__ import annotations

from duo.endpoints.order.entity.order_entity import Order

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderModel:
    user_id: int
    product_id: int
    quantity: int

    delivery_date: datetime

    id: int = None
    total_price: float = None

    def update(self, order: 'OrderModel') -> 'OrderModel':
        self.quantity = order.quantity
        self.delivery_date = order.delivery_date

        return self

    def to_entity(self) -> 'Order':
        return Order(
            id=self.id,
            user_id=self.user_id,
            product_id=self.product_id,
            quantity=self.quantity,
            total_price=self.total_price,
            delivery_date=self.delivery_date
        )

    @classmethod
    def from_entity(cls, order_entity: Order) -> 'OrderModel' | None:
        if order_entity is None:
            return None
        return cls(
            id=order_entity.id,
            user_id=order_entity.user_id,
            product_id=order_entity.product_id,
            quantity=order_entity.quantity,
            total_price=order_entity.total_price,
            delivery_date=order_entity.delivery_date
        )
