from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from models.product import Product


class ProductSchema(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str
    price: float
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductResponseSchema(BaseModel):
    product_id: str


def convert_to_product_schema(product: Product) -> ProductSchema:
    return ProductSchema(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


def convert_to_product(product_schema: ProductSchema) -> Product:
    product = Product()
    product.name = product_schema.name
    product.description = product_schema.description
    product.price = product_schema.price
    return product
