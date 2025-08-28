from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
    product_id: Optional[str] = Field(default=None)
    name: str
    price: float
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductResponseSchema(BaseModel):
    product_id: str
