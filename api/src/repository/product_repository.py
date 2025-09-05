from repository.base import BaseRepository
from models.product import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(id_field='id', filename='products.json')

    def _deserialize(self, data):
        product = Product()
        product.id = data["id"]
        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.created_at = data["created_at"]
        product.updated_at = data["updated_at"]
        return product

