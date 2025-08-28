from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class Product(BaseModel):
    id: Union[str, None] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
