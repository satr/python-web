from api.src.repository.base import BaseRepository
from api.src.models.product import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(id_field='id')

