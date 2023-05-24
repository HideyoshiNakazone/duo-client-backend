from duo.shared.exception.resource_not_found import ResourceNotFoundException
from duo.endpoints.product.repo.product_repository import ProductRepository
from duo.auth.auth_service import AuthService
from duo.endpoints.product.model.product_model import ProductModel


class ProductService:
    __slots__ = ['product_repo']

    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

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

    def search_products(self, name: str = None,
                        description: str = None,
                        price: float = None,
                        price_range=1, limit=10) -> list[ProductModel]:
        products = self.product_repo\
            .get_product_with_filters(
                name,
                description,
                price,
                price_range,
                limit
            )
        return [ProductModel.from_entity(product) for product in products]
