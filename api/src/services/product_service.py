import uuid
from datetime import datetime
from typing import Optional

from api.src.models.product import Product
from api.src.repository.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    def create_product(self, product: Product) -> str:
        product.id = str(uuid.uuid4())
        product.updated_at = product.created_at = datetime.now()
        self._product_repo.upsert(product)
        return product.id

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._product_repo.get_by_id(product_id)

    def list_products(self):
        return self._product_repo.list()

