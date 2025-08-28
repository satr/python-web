import uuid
from datetime import datetime
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from api.src.models.order import Order
from api.src.models.product import Product

app = FastAPI()
products = []
orders = []
@app.get("/")
def read_root():
    return {"hello": "world"}

@app.post("/orders")
def create_order(order: Order):
    order.orderId = str(uuid.uuid4())
    orders.append(order)
    return {"order_id": order.orderId, "order_product_id": order.productId}

@app.get("/orders/{order_id}")
def get_order_by_id(order_id: int, q: Union[str, None] = None):
    existing_order = next((order for order in orders if getattr(order, 'orderId', None) == order_id), None)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, "q": q}

@app.post("/products")
def create_product(product: Product):
    try:
        product.id = str(uuid.uuid4())
        product.updated_at = product.created_at = datetime.now()
        products.append(product)
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create Product")

@app.get("/products/{product_id}")
def get_product_by_id(product_id: str, q: Union[str, None] = None):
    existing_product = next((product for product in products if getattr(product, 'id', None) == product_id), None)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"order_id": product_id, "q": q}

@app.get("/products")
def get_products(q: Union[str, None] = None):
    return [product.model_dump() for product in products]

