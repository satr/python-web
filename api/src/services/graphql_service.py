import http
from http.client import HTTPException

from models.product import Product
from schemas.product_schema import convert_to_product_schema
from services.order_service import OrderService
from services.product_service import ProductService
import schemas.graphql_schema
from graphql import graphql_sync


class GraphQLService:
    def __init__(self, order_service: OrderService, product_service: ProductService):
        self.order_service = order_service
        self.product_service = product_service
        self.graphql_schema = schemas.graphql_schema.schema
        # self.q.type_map["Date"] = schemas.DateType
        self.graphql_schema.get_type("Mutation").fields["create_product"].resolve = self.create_product
        self.graphql_schema.get_type("Query").fields["products"].resolve = self.get_products
        self.graphql_schema.get_type("Query").fields["product"].resolve = self.get_product

    def execute_query(self, query, variables=None):
        try:
            result = graphql_sync(self.graphql_schema, query, variable_values=variables)
            return result.data
        except Exception as e:
            raise e

    def execute_mutation(self, mutation, variables=None):
        # Execute a GraphQL mutation
        pass

    def create_product(self, obj, info, input):
        if not "name" in input or not "price" in input:
            raise HTTPException(status_code=400, detail="Product name and price are required")
        product_name = input["name"]
        product = self.product_service.get_product_by_name(product_name)
        if product:
            raise HTTPException(status_code=500, detail="Product with the same name already exists")
        try:
            product = Product()
            product.name = product_name
            if "description" in input:
                product.description = input["description"]
            product.price = input["price"]
            product_id = self.product_service.create_product(product)
            return {"id": product_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_product(self, obj, info, id=None, name=None):
        if id:
            product = self.product_service.get_product(id)
        elif name:
            product = self.product_service.get_product_by_name(name)
        if not product:
            raise HTTPException(status_code=404)
        return convert_to_product_schema(product)

    def get_products(self, obj, info):
        products = self.product_service.list_products()
        return [convert_to_product_schema(product) for product in products]



