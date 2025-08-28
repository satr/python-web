import http

from fastapi import FastAPI,Response

from api.src.repository.order_repository import OrderRepository
from api.src.repository.product_repository import ProductRepository
from api.src.routes.order_routes import get_order_router
from api.src.routes.product_routes import get_product_router
from api.src.services.order_service import OrderService
from api.src.services.product_service import ProductService

app = FastAPI()

# Create one instance per repository
order_repository = OrderRepository()
product_repository = ProductRepository()

# Create one instance per service
order_service = OrderService(order_repository, product_repository)
product_service = ProductService(product_repository)

# Register routers with injected services
app.include_router(get_order_router(order_service))
app.include_router(get_product_router(product_service))

@app.get("/")
def read_root():
    return Response(content="Not Found", status_code=http.HTTPStatus.NOT_FOUND)

@app.get("/healthz")
def read_root():
    return Response(content="OK", status_code=http.HTTPStatus.OK)
