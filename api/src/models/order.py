from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel

class Order(BaseModel):
    id: Union[str, None] = None
    user_id: Union[str, None] = None
    status: Union[str, None] = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items: Optional[list['OrderItem']] = []

class OrderItem(BaseModel):
    order_id: Union[str, None] = None
    product_id: str
    quantity: Union[int, None] = 1
    price: Union[float, None] = None