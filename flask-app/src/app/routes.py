import http
import os

from flask import Blueprint, render_template
from fast_api_client.client import Client
from fast_api_client.api.products.list_products_products_get import sync_detailed as get_products_list

bp = Blueprint("routes", __name__)

@bp.route("/")
def root():
    client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
    response = get_products_list(client=client)
    products = response.parsed if response.parsed is not None else []
    return render_template("index.html", products=products)

@bp.route("/healthz")
def healthz():
    return "OK", http.HTTPStatus.OK