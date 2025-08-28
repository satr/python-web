from repository.base import BaseRepository
from models.order import Order

class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(id_field='id')

