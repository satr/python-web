from typing import Union
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}