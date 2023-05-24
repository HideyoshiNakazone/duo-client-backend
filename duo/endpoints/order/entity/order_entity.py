from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime

from duo.shared.entity import Entity


class Order(Entity):
    __tablename__ = 'order'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    delivery_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            product_id=self.product_id,
            quantity=self.quantity,
            total_price=self.total_price,
            delivery_date=self.delivery_date
        )
