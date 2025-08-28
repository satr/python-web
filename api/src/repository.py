from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, id_field: str):
        self._items: List[T] = []
        self._id_field = id_field

    def get(self) -> List[T]:
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
                return
        self._items.append(item)

