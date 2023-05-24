from duo.depends.depends_engine import get_engine
from duo.depends.depends_product import get_product_repo
from duo.endpoints.order.repo.order_repository import OrderRepository
from duo.endpoints.order.service.order_service import OrderService

from sqlalchemy.engine import Engine


def get_order_repo(engine: Engine):
    return OrderRepository(engine)


def get_order_service():
    return OrderService(
        get_order_repo(get_engine()),
        get_product_repo(get_engine())
    )
