
from typing import Any, Dict, Union, TypedDict

TypedDictMeta = TypedDict.__class__


def is_typed_dict(cls: Any) -> bool:
    return isinstance(cls, type) and issubclass(cls, dict) and cls.__class__ is TypedDictMeta


def typeddict_to_dict(cls: Any) -> Any:
    return Dict[str, Union.__getitem__(tuple(cls.__annotations__.values()))]

