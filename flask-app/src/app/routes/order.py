from flask import Blueprint, render_template
from app.clients.fast_api.fast_api_client.client import Client
from app.services.order_service import OrderService
import os

order_bp = Blueprint("orders", __name__)
api_client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
order_service = OrderService(api_client)

@order_bp.route("/order/<order_id>")
def order_detail(order_id):
    order = order_service.get_order_detail(order_id)
    return render_template("order_detail.html", order=order)


