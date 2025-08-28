import uuid
from datetime import datetime
from typing import Optional

from models.order import Order
from repository.order_repository import OrderRepository
from repository.product_repository import ProductRepository


class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self._order_repo = order_repo
        self._product_repo = product_repo

    def create_order(self, order: Order) -> str:
        order.id = str(uuid.uuid4())
        total = 0.0
        for item in order.items:
            product = self._product_repo.get_by_id(item.product_id)
            if not product:
                raise Exception(f"Product with id {item.product_id} does not exist")
            item.order_id = order.id
            item.price = product.price
            total += item.price * item.quantity
        order.total = total
        order.created_at = order.updated_at = datetime.now()
        self._order_repo.upsert(order)
        return order.id

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._order_repo.get_by_id(order_id)

    def list_orders(self):
        return self._order_repo.list()
