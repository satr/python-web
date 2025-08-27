from typing import Union
from fastapi import FastAPI

from api.src.models.item import Item

app = FastAPI()
@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}