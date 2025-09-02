import os

from jobs.order_processor.src.services.order_processor_service import OrderProcessorService


def main():
    api_url = os.getenv("API_URL", "localhost:8000")
    mq_host = os.getenv("MQ_HOST", "localhost")
    service = OrderProcessorService(api_url, mq_host)
    service.start()

if __name__ == "__main__":
    main()