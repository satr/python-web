import logging
import os
import json
import datetime
from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

LOG = logging.getLogger(__name__)

class BaseRepository(Generic[T]):
    def __init__(self, id_field: str, filename: str):
        self._items: List[T] = []
        self._id_field = id_field
        self._filename = filename
        self._data_dir = os.getenv("DATA_DIR", "./data")
        self._file_path = os.path.join(self._data_dir, self._filename)
        self._ensure_data_dir()
        self._load_from_disk()

    def _ensure_data_dir(self):
        os.makedirs(self._data_dir, exist_ok=True)

    def _load_from_disk(self):
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r") as f:
                    items = json.load(f)
                    self._items = [self._deserialize(item) for item in items]
            except Exception as ex:
                LOG.error(f"Failed to load data from {self._file_path}: {ex}")
                self._items = []

    def _save_to_disk(self):
        tmp_path = self._file_path + ".tmp"
        def to_serializable(val):
            if isinstance(val, datetime.datetime):
                return val.isoformat()
            if isinstance(val, BaseModel):
                # Use dict for Pydantic models, recursively
                return {k: to_serializable(v) for k, v in val.dict().items()}
            if hasattr(val, "__dict__"):
                # For custom objects, recursively
                return {k: to_serializable(v) for k, v in val.__dict__.items()}
            if isinstance(val, list):
                return [to_serializable(v) for v in val]
            if isinstance(val, dict):
                return {k: to_serializable(v) for k, v in val.items()}
            return val
        serializable_items = [to_serializable(item) for item in self._items]
        with open(tmp_path, "w") as f:
            json.dump(serializable_items, f)
        os.replace(tmp_path, self._file_path)

    def _serialize(self, item: T):
        def serialize_value(val):
            if isinstance(val, datetime.datetime):
                return val.isoformat()
            if isinstance(val, BaseModel):
                # Recursively serialize all fields of Pydantic models
                return {k: serialize_value(v) for k, v in val.dict().items()}
            if isinstance(val, list):
                return [serialize_value(v) for v in val]
            if isinstance(val, dict):
                return {k: serialize_value(v) for k, v in val.items()}
            return val
        # Always use .dict() for Pydantic models
        if isinstance(item, BaseModel):
            data = item.dict()
        else:
            data = item.__dict__.copy()
        return {k: serialize_value(v) for k, v in data.items()}

    def _deserialize(self, data):
        # Should be overridden in subclass if needed
        for k, v in data.items():
            if isinstance(v, str):
                try:
                    # Try to parse ISO datetime strings
                    data[k] = datetime.datetime.fromisoformat(v)
                except ValueError:
                    pass
        return data

    def list(self) -> List[T]:
        return self._items

    def get_by_id(self, item_id) -> Optional[T]:
        for item in self._items:
            if getattr(item, self._id_field, None) == item_id:
                return item
        return None

    def upsert(self, item: T):
        item_id = getattr(item, self._id_field, None)
        for idx, existing_item in enumerate(self._items):
            if getattr(existing_item, self._id_field, None) == item_id:
                self._items[idx] = item
                self._save_to_disk()
                return
        self._items.append(item)
        self._save_to_disk()
