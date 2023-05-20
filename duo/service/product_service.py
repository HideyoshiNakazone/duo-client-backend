from duo.shared.exception.resource_not_found import ResourceNotFoundException
from duo.repo.product_repository import ProductRepository
from duo.service.auth_service import AuthService
from duo.model.product_model import ProductModel


class ProductService:
    __slots__ = ['product_repo', 'auth_service']

    def __init__(self, product_repo: ProductRepository, auth_service: AuthService):
        self.product_repo = product_repo
        self.auth_service = auth_service

    def get_products(self, **kwargs) -> list[ProductModel]:
        products = self.product_repo.get_all(**kwargs)
        return [ProductModel.from_entity(product) for product in products]

    def get_product(self, product_id: int) -> ProductModel:
        product = self.product_repo.get(product_id)
        if product is None:
            raise ResourceNotFoundException(
                "Product not found."
                " Please try again with a valid product."
            )
        return ProductModel.from_entity(product)

    def add_product(self, product_model: ProductModel) -> ProductModel:
        return ProductModel.from_entity(self.product_repo.add(product_model.to_entity()))

    def update_product(self, product_id: int, product_model: ProductModel) -> ProductModel:
        product = ProductModel.from_entity(self.product_repo.get(product_id))
        if product is None:
            raise ResourceNotFoundException(
                "Product not found."
                " Please try again with a valid product."
            )
        product.update(product_model)
        return ProductModel.from_entity(self.product_repo.update(product.to_entity()))

    def remove_product(self, product_id: int) -> None:
        product = self.product_repo.get(product_id)
        if product is None:
            raise ResourceNotFoundException(
                "Product not found."
                " Please try again with a valid product."
            )
        self.product_repo.remove(product)

    def get_product_by_name(self, name: str) -> list[ProductModel]:
        products = self.product_repo.get_product_by_name(name)
        if products is None:
            raise ResourceNotFoundException(
                "Product not found."
                " Please try again with a valid product."
            )
        return [ProductModel.from_entity(product) for product in products]

    def get_product_by_description(self, description: str) -> list[ProductModel]:
        products = self.product_repo.get_product_by_description(description)
        if products is None:
            raise ResourceNotFoundException(
                "Product not found."
                " Please try again with a valid product."
            )
        return [ProductModel.from_entity(product) for product in products]

    def get_product_by_price(self, price: float, price_range=1) -> list[ProductModel]:
        products = self.product_repo.get_product_by_price(price, price_range)
        if products is None:
            raise ResourceNotFoundException(
                "Product not found."
                " Please try again with a valid product."
            )
        return [ProductModel.from_entity(product) for product in products]
