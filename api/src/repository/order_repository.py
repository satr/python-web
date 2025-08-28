from api.src.repository.base import BaseRepository
from api.src.models.order import Order

class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(id_field='id')

