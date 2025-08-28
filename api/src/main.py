import http
import uuid
from datetime import datetime
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from api.src.models.order import Order
from api.src.models.product import Product
from api.src.repository import Repository

app = FastAPI()
products_repo = Repository[Product](id_field='id')
orders_repo = Repository[Order](id_field='order_id')

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.post("/orders")
def create_order(order: Order):
    try:
        if len(order.items) == 0:
            raise HTTPException(status_code=500, detail="Order must have at least one item")
        order.id = str(uuid.uuid4())

        for item in order.items:
            product = products_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with id {item.product_id} does not exist")
            item.order_id = order.id
            item.price = product.price

        order.updated_at = order.created_at = datetime.now()
        orders_repo.upsert(order)
        return JSONResponse(content={"order_id": order.id}, status_code=http.HTTPStatus.CREATED)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to create Order {str(ex)}")

@app.get("/orders/{order_id}")
def get_order_by_id(order_id: str, q: Union[str, None] = None):
    try:
        existing_order = orders_repo.get_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return JSONResponse(content=existing_order.model_dump(), status_code=http.HTTPStatus.OK)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to get Order {str(ex)}")


@app.get("/orders")
def get_orders(q: Union[str, None] = None):
    try:
        return [order.model_dump() for order in orders_repo.get()]
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to get Orders {str(ex)}")

@app.post("/products")
def create_product(product: Product):
    product.id = str(uuid.uuid4())
    try:
        products_repo.upsert(product)
        return JSONResponse(content={"product_id": product.id}, status_code=http.HTTPStatus.CREATED)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to create Product {str(ex)}")

@app.get("/products/{product_id}")
def get_product_by_id(product_id: str, q: Union[str, None] = None):
    try:
        existing_product = products_repo.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return JSONResponse(content=existing_product.model_dump(), status_code=http.HTTPStatus.OK)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to create Product {str(ex)}")

@app.get("/products")
def get_products(q: Union[str, None] = None):
    try:
        return [product.model_dump() for product in products_repo.get()]
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to get Products {str(ex)}")