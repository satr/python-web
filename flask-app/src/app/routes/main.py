from flask import Blueprint, render_template, request
from app.clients.fast_api.fast_api_client.client import Client
from app.services.product_service import ProductService
from app.services.order_service import OrderService
import os

main_bp = Blueprint("main", __name__)
api_client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
product_service = ProductService(api_client)
order_service = OrderService(api_client)

@main_bp.route("/", methods=["GET", "POST"])
def home():
    products = product_service.get_products()
    orders = order_service.get_orders()
    order_result = None

    if request.method == "POST":
        items = order_service.parse_order_form(request.form, products)
        if items:
            result = order_service.create_order(items)
            order_result = "Order created successfully!" if result else "Order creation failed."
            orders = order_service.get_orders()
        else:
            order_result = "No products selected."
    return render_template("index.html", products=products, orders=orders, order_result=order_result)

@main_bp.route("/healthz")
def healthz():
    return "OK", 200

