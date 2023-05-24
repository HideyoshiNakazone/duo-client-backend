from duo.endpoints.order.model.order_model import OrderModel
from duo.endpoints.order.repo.order_repository import OrderRepository
from duo.endpoints.product.repo.product_repository import ProductRepository
from duo.shared.exception.invalid_resource_exception import InvalidResourceException


class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repository: ProductRepository):
        self.order_repo = order_repo
        self.product_repository = product_repository

    def get_orders(self, **kwargs):
        return [
            OrderModel.from_entity(order)
            for order in self.order_repo.get_all(**kwargs)
        ]

    def get_order(self, order_id: int):
        return self.order_repo.get(order_id)

    def get_orders_for_user_by_id(self, user_id: int):
        return self.order_repo\
            .get_orders_for_user_by_id(user_id)

    def add_order(self, order: OrderModel):
        product = self.product_repository.get(order.product_id)
        if product is None:
            raise InvalidResourceException(f'Product with id {order.product_id} does not exist')

        order.total_price = product.price * order.quantity
        return OrderModel.from_entity(
            self.order_repo.add(order.to_entity())
        )

    def update_order(self, new_order: OrderModel):
        order = OrderModel.from_entity(
            self.order_repo.get(new_order.id)
        )
        if order is None:
            raise InvalidResourceException(f'Order with id {new_order.id} does not exist')

        product = self.product_repository.get(new_order.product_id)
        if product is None:
            raise InvalidResourceException(f'Product with id {new_order.product_id} does not exist')

        new_order.total_price = product.price * new_order.quantity

        return OrderModel.from_entity(
            self.order_repo.update(order.update(new_order).to_entity())
        )

    def delete_order(self, order_id: int):
        order = self.order_repo.get(order_id)
        if order is None:
            raise InvalidResourceException(f'Order with id {order_id} does not exist')

        self.order_repo.remove(order.id)
