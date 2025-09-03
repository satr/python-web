import uuid
import time
import logging
from datetime import datetime
from typing import Optional
import threading
import pika

from models.order import Order
from repository.order_repository import OrderRepository
from repository.product_repository import ProductRepository
from pika.exceptions import AMQPConnectionError, AMQPError, StreamLostError, ChannelClosedByBroker

LOG = logging.getLogger(__name__)

class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository, mq_host):
        self._order_repo = order_repo
        self._product_repo = product_repo
        self._mq_publisher = MQPublisher(mq_host=mq_host, queue_name="orders")

    def upsert_order(self, order: Order) -> str:
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

    def _publish_new_order(self, id):
        self._mq_publisher.publish(id.encode())

    def get_order(self, id: str) -> Optional[Order]:
        return self._order_repo.get_by_id(id)

    def list_orders(self):
        return self._order_repo.list()


class MQPublisher:
    def __init__(self, mq_host: str, queue_name="orders", durable=True,
                 max_retries=5, base_backoff=0.5):
        self._queue = queue_name
        self._durable = durable
        self._max_retries = max_retries
        self._base_backoff = base_backoff
        self._conn = None
        self._ch = None

        params = pika.URLParameters(f'amqp://guest:guest@{mq_host}')
        params.heartbeat = 30
        params.blocked_connection_timeout = 60
        self._params = params

    def _connect(self):
        if self._conn and self._conn.is_open:
            return
        self._conn = pika.BlockingConnection(self._params)
        self._ch = self._conn.channel()
        self._ch.queue_declare(queue=self._queue, durable=self._durable)
        self._ch.confirm_delivery()

    def _close(self):
        for x in (self._ch, self._conn):
            try:
                if x and x.is_open: x.close()
            except Exception as ex:
                LOG.error(f"Error closing connection: {ex}")

        self._ch = self._conn = None

    def publish(self, body: bytes) -> bool:
        for attempt in range(self._max_retries):
            try:
                if not self._ch or self._ch.is_closed:
                    self._connect()
                props = pika.BasicProperties(delivery_mode=2)  # persistent
                self._ch.basic_publish("", self._queue, body, properties=props)
                return True
            except (AMQPConnectionError, AMQPError, OSError, StreamLostError, ChannelClosedByBroker) as ex:
                LOG.warning("Publish failed, retrying (attempt %s/%s): %s", attempt+1, self._max_retries, ex)
                self._close()
                time.sleep(self._base_backoff * (2 ** attempt))
        return False