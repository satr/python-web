import pika

from app.clients.fast_api.fast_api_client import Client
from app.clients.fast_api.fast_api_client.api.orders.create_order_orders_post import sync_detailed as create_order
from app.clients.fast_api.fast_api_client.api.orders.get_order_orders_id_get import   sync_detailed as get_order


class OrderProcessorService:
    def __init__(self, api_url, mq_host):
        self._api_client = Client(base_url=api_url)
        self._mq_channel = self.get_mq_consume_channel(mq_host)

    def get_mq_consume_channel(self, mq_host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
        channel = connection.channel()
        channel.queue_declare(queue='orders', durable=True)
        channel.basic_consume(queue='orders', on_message_callback=self.process_order_message, auto_ack=True)
        return channel

    def start(self):
        self._mq_channel.start_consuming()

    def process_order_message(self, ch, method, properties, body):
        try:
            id = body.decode()
            order_result = get_order(client=self._api_client, id=id)
            order = order_result.parsed
            if not order:
                raise Exception(f'Order not found by id {id}')
            order.status = 'completed'
            create_order(client=self._api_client, body=order)
        except Exception as ex:
            print(ex)

