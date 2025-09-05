from repository.base import BaseRepository
from models.order import Order
from datetime import datetime

class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(id_field='id', filename='orders.json')

    def _deserialize(self, data):
        # Only convert known datetime fields
        for field in ['created_at', 'updated_at']:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except ValueError:
                    pass
        return Order.parse_obj(data)
