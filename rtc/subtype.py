
from typing import Any, Tuple, TypeVar, Union, Hashable, Sized, _SpecialForm, Generic
from collections.abc import Callable, Iterable, Container, Reversible, Coroutine, Generator, AsyncGenerator

from .tools import is_typed_dict, typeddict_to_dict


def check_list(frst: Any, scnd: Any) -> bool:
    if frst.__args__ == scnd.__args__:
        return True
    if len(scnd.__args__) == 1 and isinstance(scnd.__args__[0], TypeVar) and scnd.__args__[0].__name__ == 'T':
        return True
    for arg1 in frst.__args__:
        if not any(is_subtype(arg1, arg2) for arg2 in scnd.__args__):
            return False
    return True


def check_tuple(frst: Any, scnd: Any) -> bool:
    if frst.__args__ == scnd.__args__:
        return True
    if not scnd.__args__:
        return True
    if not frst.__args__ and scnd.__args__:
        return False
    if len(scnd.__args__) == 1:
        return all(is_subtype(arg1, scnd.__args__[0]) for arg1 in frst.__args__)
    if len(frst.__args__) != len(scnd.__args__):
        return False
    for i in range(len(frst.__args__)):
        if not is_subtype(frst.__args__[i], scnd.__args__[i]):
            return False
    return True


def check_union(frst: Any, scnd: Any) -> bool:
    if getattr(frst, '__origin__', None) == Union:
        for i in range(len(scnd.__args__)):
            if scnd.__args__[i] is None:
                scnd.__args__[i] = type(None)
        for arg1 in frst.__args__:
            if arg1 is None:
                arg1 = type(None)
            if not any(is_subtype(arg1, arg) for arg in scnd.__args__):
                return False
        return True
    return any(is_subtype(frst, arg) for arg in scnd.__args__)


def check_dict(frst: Any, scnd: Any) -> bool:
    key1, key2 = frst.__args__[0], scnd.__args__[0]
    if isinstance(key1, TypeVar) and key1.__name__ == 'KT':
        key1 = Any
    if isinstance(key2, TypeVar) and key2.__name__ == 'KT':
        key2 = Any
    if not is_subtype(key1, key2):
        return False
    val1, val2 = frst.__args__[1], scnd.__args__[1]
    if isinstance(val1, TypeVar) and val1.__name__ == 'VT':
        val1 = Any
    if isinstance(val2, TypeVar) and val2.__name__ == 'VT':
        val2 = Any
    return is_subtype(val1, val2)


def check_callable(frst: Any, scnd: Any) -> bool:
    if len(frst.__args__) != len(scnd.__args__):
        return False
    return all(is_subtype(frst.__args__[i], scnd.__args__[i]) for i in range(len(frst.__args__)))


def check_iterable(frst: Any, scnd: Any) -> bool:
    if isinstance(frst, type):
        return hasattr(tuple, '__iter__')
    if isinstance(scnd.__args__[0], TypeVar):
        return True
    return is_subtype(frst.__args__[0], scnd.__args__[0])


def check_alias(attr: str):
    return lambda frst, scnd: (
        isinstance(frst, type) and getattr(frst, attr, None)
    ) or (
        (
            is_subtype(frst.__origin__, scnd)
        ) if not isinstance(frst.__origin__, _SpecialForm) else (
            all(
                is_subtype(arg, scnd)
                for arg in frst.__args__
            )
        )
    )


def check_yielder(type_vars: Tuple[str, ...]):
    def check(frst: Any, scnd: Any) -> bool:
        if scnd.__origin__ != frst.__origin__:
            return False
        if tuple(
            arg.__name__
            for arg in scnd.__args__
            if isinstance(arg, TypeVar)
        ) == type_vars:
            return True
        return all(
            is_subtype(frst.__args__[i], scnd.__args__[i])
            for i in range(len(type_vars))
        )
    return check


def check_generic(frst: Any, scnd: Any) -> bool:
    return issubclass(frst.__origin__, scnd.__origin__) and (
        len(frst.__args__) == len(scnd.__args__) and all(
            is_subtype(frst.__args__[i], scnd.__args__[i])
            for i in range(len(frst.__args__))
        )
    )


def check_typeddict(frst: Any, scnd: Any) -> bool:
    if isinstance(scnd, type) and issubclass(scnd, dict) and hasattr(scnd, '__annotations__'):
        for key, key_type in scnd.__annotations__.items():
            if key not in frst.__annotations__ or not is_subtype(frst.__annotations__[key], key_type):
                return False
    elif hasattr(scnd, '__origin__'):
        key1 = scnd.__args__[0]
        key2 = scnd.__args__[1]
        if isinstance(key1, TypeVar) and key1.__name__ == 'KT':
            key1 = Any
        if isinstance(key2, TypeVar) and key2.__name__ == 'VT':
            key2 = Any
        if not is_subtype(str, key1):
            return False
        return all(is_subtype(key_type, key2) for key, key_type in frst.__annotations__.items())
    return True


SUBTYPE_CHECK_HANDLERS = {
    list: check_list,
    tuple: check_tuple,
    dict: check_dict,
    set: check_list,
    Union: check_union,
    Callable: check_callable,
    Iterable: check_iterable,
    Hashable: check_alias('__hash__'),
    Sized: check_alias('__len__'),
    Container: check_alias('__contains__'),
    Reversible: check_alias('__reversed__'),
    Coroutine: check_yielder(('T_co', 'T_contra', 'V_co')),
    Generator: check_yielder(('T_co', 'T_contra', 'V_co')),
    AsyncGenerator: check_yielder(('T_co', 'T_contra')),
    Generic: check_generic,
}


def is_subtype(frst: Any, scnd: Any) -> bool:
    """
        return True if 'frst' is subtype of 'scnd'
        Example:
            List[str], List -> True
            bool, int -> True
            bool, bool -> True
            int, bool -> False
            Optional[str], Union[str, int, None] -> True
            List[str], List[int] -> False
    """
    frst = type(None) if frst is None else frst
    scnd = type(None) if scnd is None else scnd
    if is_typed_dict(scnd) + is_typed_dict(frst) == 1:
        scnd = typeddict_to_dict(scnd) if is_typed_dict(scnd) else scnd
        frst = typeddict_to_dict(frst) if is_typed_dict(frst) else frst
    if isinstance(frst, type) and isinstance(scnd, type) and not is_typed_dict(scnd):
        return issubclass(frst, scnd)
    if Any == scnd or Any == frst:
        return scnd == Any
    if isinstance(scnd, TypeVar) or isinstance(frst, TypeVar):
        return isinstance(scnd, TypeVar) and isinstance(frst, TypeVar) and scnd.__name__ == frst.__name__
    if hasattr(frst, '__origin__') and isinstance(frst.__origin__, type) and isinstance(scnd, type) and not is_typed_dict(scnd):
        return issubclass(frst.__origin__, scnd)
    if hasattr(scnd, '__origin__') and isinstance(scnd.__origin__, type) and isinstance(frst, type) and not is_typed_dict(frst):
        return issubclass(frst, scnd.__origin__)
    if is_typed_dict(frst):
        handler = check_typeddict
    elif hasattr(scnd, '__origin__'):
        handler = (SUBTYPE_CHECK_HANDLERS.get(scnd.__origin__) or SUBTYPE_CHECK_HANDLERS.get(scnd)) or check_generic
    else:
        handler = lambda x, y: x == y
    return handler(frst, scnd)
