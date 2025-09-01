from http.client import HTTPException

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
        self.graphql_schema.get_type("Query").fields["product"].resolve = self.get_product
        self.graphql_schema.get_type("Query").fields["products"].resolve = self.get_products
        pass

    def execute_query(self, query, variables=None):
        try:
            result = graphql_sync(self.graphql_schema, query, variable_values=variables)
            return result.data
        except Exception as e:
            raise e

    def execute_mutation(self, mutation, variables=None):
        # Execute a GraphQL mutation
        pass

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



