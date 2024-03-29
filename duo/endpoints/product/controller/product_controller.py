from duo.depends.depends_product import get_product_service
from duo.depends.depends_session import get_session_service
from duo.depends.depends_user import get_user_service
from duo.endpoints.product.model.product_model import ProductModel
from duo.endpoints.product.service.product_service import ProductService
from duo.endpoints.session.service.session_service import SessionService
from duo.endpoints.user.service.user_service import UserService

from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, Request, Response
from fastapi_utils.cbv import cbv

from typing import Optional


product_router = InferringRouter()


@cbv(product_router)
class UserController:
    product_service: ProductService = Depends(get_product_service, use_cache=True)
    session_service: SessionService = Depends(get_session_service, use_cache=True)

    @product_router.get("/product", status_code=200)
    def get_products(self, name: Optional[str] = None,
                     description: Optional[str] = None,
                     price: Optional[float] = None) -> list[ProductModel]:
        return self.product_service.get_products(
            name=name,
            description=description,
            price=price
        )

    @product_router.get("/product/search", status_code=200)
    def search_products(self, name: Optional[str] = None,
                        description: Optional[str] = None,
                        price: Optional[float] = None,
                        price_rance: Optional[int] = 1) -> list[ProductModel]:
        return self.product_service.search_products(
            name=name,
            description=description,
            price=price,
            price_range=price_rance
        )

    @product_router.post("/product", status_code=201)
    def add_product(self, request: Request, response: Response,
                    product_model: ProductModel) -> ProductModel:
        self.session_service.from_request(request, response) \
            .validate_is_admin()
        return self.product_service.add_product(product_model)

    @product_router.get("/product/{product_id}", status_code=200)
    def get_product(self, product_id: int) -> ProductModel:
        return self.product_service.get_product(product_id)

    @product_router.put("/product/{product_id}", status_code=200)
    def update_product(self, request: Request, response: Response,
                       product_id: int, product_model: ProductModel) -> ProductModel:
        self.session_service.from_request(request, response) \
            .validate_is_admin()
        return self.product_service.update_product(product_id, product_model)

    @product_router.delete("/product/{product_id}", status_code=204)
    def remove_product(self, request: Request, response: Response,
                       product_id: int):
        self.session_service.from_request(request, response) \
            .validate_is_admin()
        self.product_service.remove_product(product_id)
