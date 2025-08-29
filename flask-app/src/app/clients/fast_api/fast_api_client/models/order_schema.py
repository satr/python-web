import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.order_item_schema import OrderItemSchema


T = TypeVar("T", bound="OrderSchema")


@_attrs_define
class OrderSchema:
    """
    Attributes:
        items (list['OrderItemSchema']):
        order_id (Union[None, Unset, str]):
        user_id (Union[None, Unset, str]):
        created_at (Union[None, Unset, datetime.datetime]):
        updated_at (Union[None, Unset, datetime.datetime]):
        total (Union[None, Unset, float]):
        status (Union[None, Unset, str]):
    """

    items: list["OrderItemSchema"]
    order_id: Union[None, Unset, str] = UNSET
    user_id: Union[None, Unset, str] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    total: Union[None, Unset, float] = UNSET
    status: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        order_id: Union[None, Unset, str]
        if isinstance(self.order_id, Unset):
            order_id = UNSET
        else:
            order_id = self.order_id

        user_id: Union[None, Unset, str]
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        total: Union[None, Unset, float]
        if isinstance(self.total, Unset):
            total = UNSET
        else:
            total = self.total

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if order_id is not UNSET:
            field_dict["order_id"] = order_id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if total is not UNSET:
            field_dict["total"] = total
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.order_item_schema import OrderItemSchema

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = OrderItemSchema.from_dict(items_item_data)

            items.append(items_item)

        def _parse_order_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        order_id = _parse_order_id(d.pop("order_id", UNSET))

        def _parse_user_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_total(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total = _parse_total(d.pop("total", UNSET))

        def _parse_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        status = _parse_status(d.pop("status", UNSET))

        order_schema = cls(
            items=items,
            order_id=order_id,
            user_id=user_id,
            created_at=created_at,
            updated_at=updated_at,
            total=total,
            status=status,
        )

        order_schema.additional_properties = d
        return order_schema

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
