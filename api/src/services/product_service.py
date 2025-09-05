import uuid
from datetime import datetime
from typing import Optional

from models.product import Product
from repository.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    def upsert_product(self, product: Product) -> str:
        existing_product = self.get_product_by_name(product.name)
        if existing_product:
            product.id = existing_product.id
            product.created_at = existing_product.created_at
        else:
            product.id = str(uuid.uuid4())
            product.created_at = datetime.now()
        product.updated_at  = datetime.now()
        self._product_repo.upsert(product)
        return product.id

    def get_product(self, id: str) -> Optional[Product]:
        return self._product_repo.get_by_id(id)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        products = self._product_repo.list()
        if len(products) == 0:
            return None
        try:
            return next(product for product in products if product.name == name)
        except StopIteration:
            return None

    def list_products(self):
        return self._product_repo.list()

