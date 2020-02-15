
from typing import Any, TypeVar, Union
from collections.abc import Callable, Iterable


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
    for arg1 in frst.__args__:
        if not any(is_subtype(arg1, arg2) for arg2 in scnd.__args__):
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


SUBTYPE_CHECK_HANDLERS = {
    list: check_list,
    tuple: check_tuple,
    dict: check_dict,
    Union: check_union,
    Callable: check_callable,
    Iterable: check_iterable,
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
    if isinstance(frst, type) and isinstance(scnd, type):
        return issubclass(frst, scnd)
    if Any in {scnd, frst}:
        return scnd == Any
    if isinstance(scnd, TypeVar) or isinstance(frst, TypeVar):
        return isinstance(scnd, TypeVar) and isinstance(frst, TypeVar) and scnd.__name__ == frst.__name__
    if hasattr(frst, '__origin__') and isinstance(frst.__origin__, type) and isinstance(scnd, type):
        return issubclass(frst.__origin__, scnd)
    if hasattr(scnd, '__origin__') and isinstance(scnd.__origin__, type) and isinstance(frst, type):
        return issubclass(frst, scnd.__origin__)
    return (
        (SUBTYPE_CHECK_HANDLERS.get(scnd.__origin__) or SUBTYPE_CHECK_HANDLERS.get(scnd))(frst, scnd)
        if hasattr(scnd, '__origin__') else
        frst == scnd
    )
