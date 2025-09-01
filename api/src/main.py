import http

from fastapi import FastAPI,Response

from repository.order_repository import OrderRepository
from repository.product_repository import ProductRepository
from routes.graphql_routes import get_graphql_router
from routes.order_routes import get_order_router
from routes.product_routes import get_product_router
from services.graphql_service import GraphQLService
from services.order_service import OrderService
from services.product_service import ProductService

app = FastAPI()

order_repository = OrderRepository()
product_repository = ProductRepository()

order_service = OrderService(order_repository, product_repository)
product_service = ProductService(product_repository)
graph_ql_service = GraphQLService(order_service, product_service)

app.include_router(get_order_router(order_service))
app.include_router(get_product_router(product_service))
app.include_router(get_graphql_router(graph_ql_service))

@app.get("/")
def read_root():
    return Response(content="Not Found", status_code=http.HTTPStatus.NOT_FOUND)

@app.get("/healthz")
def read_root():
    return Response(content="OK", status_code=http.HTTPStatus.OK)
