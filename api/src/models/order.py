from datetime import datetime
from typing import List

class Order:
    id: str
    user_id: str
    status: str = "pending"
    created_at: datetime
    updated_at: datetime
    items: List['OrderItem']
    total: float

class OrderItem:
    order_id: str
    product_id: str
    quantity: int
    price: float
