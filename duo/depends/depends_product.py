from duo.depends.depends_engine import get_engine
from duo.depends.depends_user import get_auth_service
from duo.repo.product_repository import ProductRepository
from duo.service.product_service import ProductService

from sqlalchemy.engine import Engine


def get_product_repo(engine: Engine) -> ProductRepository:
    return ProductRepository(engine)


def get_product_service() -> ProductService:
    return ProductService(
        get_product_repo(get_engine()),
        get_auth_service()
    )