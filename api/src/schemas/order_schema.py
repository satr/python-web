from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItemSchema(BaseModel):
    product_id: str
    quantity: int
    price: Optional[float] = None

class OrderSchema(BaseModel):
    id: Optional[str] = Field(default=None)
    items: List[OrderItemSchema]
    user_id: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total: Optional[float] = None
    status: Optional[str] = None

class OrderResponseSchema(BaseModel):
    id: str