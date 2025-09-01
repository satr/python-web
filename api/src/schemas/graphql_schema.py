# from datetime import datetime, date
from typing import Dict, Optional, Any
from pydantic import BaseModel

from graphql import build_schema, GraphQLError, GraphQLScalarType

class GraphQLRequest(BaseModel):
    query: str
    variables: Optional[Dict[str, Any]] = None
    operationName: Optional[str] = None

# # Custom Date scalar
# def serialize_date(value):
#     if isinstance(value, (date, datetime)):
#         return value.isoformat()
#     raise GraphQLError("Date cannot represent non-date value: " + repr(value))
#
# def parse_date_value(value):
#     try:
#         return date.fromisoformat(value)
#     except Exception:
#         raise GraphQLError("Date cannot represent value: " + repr(value))
#
# DateType = GraphQLScalarType(
#     name="Date",
#     description="ISO-8601 formatted date",
#     serialize=serialize_date,
#     parse_value=parse_date_value,
# )

schema = build_schema("""
  type Product {
    id: ID
    name: String!
    price: Float!
    description: String
    created_at: String
    updated_at: String
  }

  input ProductInput {
    name: String!
    description: String
    price: Float!
  }

  input OrderInput {
    productId: ID!
    quantity: Int!
  }

  type ProductResponse {
    id: ID!
  }

  type OrderResponse {
    orderId: ID!
  }

  type Query {
    products: [Product!]!
    product(id: ID, name: String): Product
  }

  type Mutation {
    createProduct(input: ProductInput!): ProductResponse!
    createOrder(input: OrderInput!): OrderResponse!
  }
""")
# graphql_schema.type_map["Date"] = DateType