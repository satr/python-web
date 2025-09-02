import uuid
from datetime import datetime
from typing import Optional
import threading
import pika

from models.order import Order
from repository.order_repository import OrderRepository
from repository.product_repository import ProductRepository


class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository, mq_host):
        self._order_repo = order_repo
        self._product_repo = product_repo
        self._mq_host = mq_host
        self._mq_publish_connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
        self._mq_publish_channel = self._mq_publish_connection.channel()
        self._mq_publish_channel.queue_declare(queue='orders')

    def create_order(self, order: Order) -> str:
        is_new = not hasattr(order, "id") or order.id is None
        if is_new:
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
        else:
            order.updated_at = datetime.now()
        self._order_repo.upsert(order)

        if is_new:
            # Non-blocking publish using a thread
            threading.Thread(target=self._publish_new_order, args=(order.id,), daemon=True).start()

        return order.id

    def _publish_new_order(self, order_id):
        if self._mq_publish_channel.is_open:
            self._mq_publish_channel.basic_publish(exchange='', routing_key='orders', body=str(order_id))
        else:
            print("MQ channel is closed, cannot publish order")

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._order_repo.get_by_id(order_id)

    def list_orders(self):
        return self._order_repo.list()
