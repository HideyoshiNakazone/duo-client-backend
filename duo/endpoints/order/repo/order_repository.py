from duo.endpoints.order.entity.order_entity import Order
from duo.shared.repository import SQLRepository

from sqlalchemy.orm import Session


class OrderRepository(SQLRepository):
    entity = Order

    def get_orders_for_user_by_id(self, user_id: int):
        with Session(self.engine) as session:
            return session.query(self.entity) \
                .filter(self.entity.user_id == user_id) \
                .all()
