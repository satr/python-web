from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.graph_ql_request_variables_type_0 import GraphQLRequestVariablesType0


T = TypeVar("T", bound="GraphQLRequest")


@_attrs_define
class GraphQLRequest:
    """
    Attributes:
        query (str):
        variables (Union['GraphQLRequestVariablesType0', None, Unset]):
        operation_name (Union[None, Unset, str]):
    """

    query: str
    variables: Union["GraphQLRequestVariablesType0", None, Unset] = UNSET
    operation_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.graph_ql_request_variables_type_0 import GraphQLRequestVariablesType0

        query = self.query

        variables: Union[None, Unset, dict[str, Any]]
        if isinstance(self.variables, Unset):
            variables = UNSET
        elif isinstance(self.variables, GraphQLRequestVariablesType0):
            variables = self.variables.to_dict()
        else:
            variables = self.variables

        operation_name: Union[None, Unset, str]
        if isinstance(self.operation_name, Unset):
            operation_name = UNSET
        else:
            operation_name = self.operation_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if variables is not UNSET:
            field_dict["variables"] = variables
        if operation_name is not UNSET:
            field_dict["operationName"] = operation_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.graph_ql_request_variables_type_0 import GraphQLRequestVariablesType0

        d = dict(src_dict)
        query = d.pop("query")

        def _parse_variables(data: object) -> Union["GraphQLRequestVariablesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                variables_type_0 = GraphQLRequestVariablesType0.from_dict(data)

                return variables_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GraphQLRequestVariablesType0", None, Unset], data)

        variables = _parse_variables(d.pop("variables", UNSET))

        def _parse_operation_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        operation_name = _parse_operation_name(d.pop("operationName", UNSET))

        graph_ql_request = cls(
            query=query,
            variables=variables,
            operation_name=operation_name,
        )

        graph_ql_request.additional_properties = d
        return graph_ql_request

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
