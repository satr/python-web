from flask import Blueprint, render_template, request
from app.clients.fast_api.fast_api_client.client import Client
from app.services.product_service import ProductService
import os

product_bp = Blueprint("products", __name__)
api_client = Client(base_url=os.getenv("API_URL", "http://localhost:8000"))
product_service = ProductService(api_client)

@product_bp.route("/products", methods=["GET", "POST"])
def product_details():
    product_result = ""
    if request.method == "POST":
        product = product_service.get_product_from_request(request)
        response = product_service.post_product(product)
        product_result = "Product created successfully!" if response else "Product creation failed."
    return render_template("product_detail.html", product_result=product_result, editable=request.method == "GET")


