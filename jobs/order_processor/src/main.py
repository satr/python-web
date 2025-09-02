import os

import pika


def main():
    mq_host = os.getenv("MQ_HOST", "localhost")
    api_url = os.getenv("API_URL", "localhost:8000")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
    channel = connection.channel()
    channel.queue_declare(queue='orders')
    channel.basic_consume(queue='orders', on_message_callback=process_order_message, auto_ack=True)
    channel.start_consuming()

def process_order_message(ch, method, properties, body):
    print("Received order message:", body)

if __name__ == "__main__":
    main()