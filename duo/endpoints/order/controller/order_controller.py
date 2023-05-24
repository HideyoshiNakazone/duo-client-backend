from duo.endpoints.session.service.session_service import SessionService
from duo.endpoints.order.service.order_service import OrderService
from duo.endpoints.order.model.order_model import OrderModel
from duo.depends.depends_session import get_session_service
from duo.depends.depends_order import get_order_service

from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, Request, Response
from fastapi_utils.cbv import cbv

from datetime import datetime


order_router = InferringRouter()


@cbv(order_router)
class OrderController:
    order_service: OrderService = Depends(get_order_service, use_cache=True)
    session_service: SessionService = Depends(get_session_service, use_cache=True)

    @order_router.get("/order", status_code=200)
    def get_orders(self, user_id: int,
                   product_id: int,
                   quantity: int,
                   delivery_date: datetime,
                   total_price: float,
                   request: Request,
                   response: Response) -> list[OrderModel]:
        self.session_service.from_request(request, response) \
            .validate_is_admin()
        return self.order_service.get_orders(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            delivery_date=delivery_date,
            total_price=total_price
        )

    @order_router.get("/order/{order_id}", status_code=200)
    def get_order(self, request: Request, response: Response,
                  order_id: int) -> OrderModel:
        order = self.order_service.get_order(order_id)

        self.session_service.from_request(request, response) \
            .validate_same_user(order.user_id)

        return order

    @order_router.get("/order/user/{user_id}", status_code=200)
    def get_orders_for_user_by_id(self, request: Request, response: Response,
                                  user_id: int) -> list[OrderModel]:
        self.session_service.from_request(request, response) \
            .validate_same_user(user_id)

        return self.order_service.get_orders_for_user_by_id(user_id)

    @order_router.post("/order", status_code=201)
    def add_order(self, request: Request, response: Response,
                  order_model: OrderModel) -> OrderModel:
        self.session_service.from_request(request, response) \
            .validate_same_user(order_model.user_id)

        return self.order_service.add_order(order_model)

    @order_router.put("/order/{order_id}", status_code=200)
    def update_order(self, request: Request, response: Response,
                     order_id: int, order_model: OrderModel) -> OrderModel:
        order = self.order_service.get_order(order_id)

        self.session_service.from_request(request, response) \
            .validate_same_user(order.user_id)

        order_model.id = order_id
        return self.order_service.update_order(order_model)

    @order_router.delete("/order/{order_id}", status_code=200)
    def delete_order(self, request: Request, response: Response,
                     order_id: int) -> OrderModel:
        order = self.order_service.get_order(order_id)

        self.session_service.from_request(request, response) \
            .validate_same_user(order.user_id)

        return self.order_service.delete_order(order_id)
