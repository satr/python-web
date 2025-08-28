from typing import Union

from pydantic import BaseModel

class Order(BaseModel):
    orderId: Union[str, None] = None
    userId: Union[str, None] = None
    status: Union[str, None] = "pending"
    createdAt: Union[str, None] = None
    updatedAt: Union[str, None] = None

class OrderItem(BaseModel):
    productId: Union[str, None] = None
    quantity: Union[int, None] = 1
    price: Union[float, None] = None