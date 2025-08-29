import http
import os
from flask import Blueprint, render_template, request
from fast_api_client.client import Client
from fast_api_client.api.products.list_products_products_get import sync_detailed as get_products_list
from fast_api_client.api.orders.list_orders_orders_get import sync_detailed as get_orders_list
from fast_api_client.api.orders.create_order_orders_post import sync_detailed as create_order
from fast_api_client.models.order_schema import OrderSchema
from fast_api_client.models.order_item_schema import OrderItemSchema

bp = Blueprint("routes", __name__)

@bp.route("/", methods=["GET"])
def home():
    client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
    products = get_products(client)
    orders = get_orders(client)
    order_result = None
    return render_template("index.html", products=products, orders=orders, order_result=order_result)

@bp.route("/", methods=["POST"])
def post_order():
    client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
    products = get_products(client)
    items = []
    for product in products:
        product_id = getattr(product, "product_id", None)
        quantity = int(request.form.get(f"quantity_{product_id}", 0))
        price = float(request.form.get(f"price_{product_id}", 0))
        if quantity > 0:
            item = OrderItemSchema(product_id=product_id, quantity=quantity, price=price)
            items.append(item)
    if items:
        order = OrderSchema(items=items)
        order_response = create_order(client=client, body=order)
        if order_response.parsed:
            order_result = "Order created successfully!"
            orders = get_orders(client)
        else:
            order_result = "Order creation failed."
            orders = get_orders(client)
    else:
        order_result = "No products selected."
        orders = get_orders(client)

    return render_template("index.html", products=products, orders=orders, order_result=order_result)


def get_products(client):
    product_list_response = get_products_list(client=client)
    products = product_list_response.parsed if product_list_response.parsed is not None else []
    return products


def get_orders(client):
    order_list_response = get_orders_list(client=client)
    orders = order_list_response.parsed if order_list_response.parsed is not None else []
    return orders


@bp.route("/healthz")
def healthz():
    return "OK", http.HTTPStatus.OK

@bp.route("/order/<order_id>")
def order_detail(order_id):
    client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
    from fast_api_client.api.orders.get_order_orders_order_id_get import sync_detailed as get_order_detail
    response = get_order_detail(client=client, order_id=order_id)
    order = response.parsed if response.parsed is not None else None
    return render_template("order_detail.html", order=order)
