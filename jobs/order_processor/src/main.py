import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from services.order_processor_service import OrderProcessorService


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")


def run_health_server():
    port = int(os.getenv("HEALTH_PORT", "8002"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


def main():
    api_url = os.getenv("API_URL", "localhost:8000")
    mq_host = os.getenv("MQ_HOST", "localhost")
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    service = OrderProcessorService(api_url, mq_host)
    service.start()


if __name__ == "__main__":
    main()