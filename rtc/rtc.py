
import asyncio
from typing import Tuple, List, Dict, Any, Optional, Union, Callable, TypeVar
from collections import abc

from .subtype import is_subtype

T = TypeVar('T')

CheckerType = Tuple[bool, Optional[str]]


def check_union(value: T, typo: Any) -> CheckerType:
    for type_ in typo.__args__:
        if check_type(value, type_)[0]:
            return True, None
    return False, 'expected value any type of [%s], got "%s"' % (typo.__args__, value)


def check_list(value: T, typo: Any) -> CheckerType:
    if isinstance(typo, type) and not isinstance(value, typo):
        return False, 'expected "%s", got "%s"' % (typo, type(value))
    if hasattr(typo, '__origin__'):
        if not isinstance(value, typo.__origin__):
            return False, 'expected "%s", got "%s"' % (typo, type(value))
        if typo.__args__:
            for i in value:
                if not (res := check_type(i, typo.__args__))[0]:
                    return res
    return True, None


def check_tuple(value: T, typo: Any) -> CheckerType:
    if isinstance(typo, type) and not isinstance(value, typo):
        return False, 'expected "%s", got "%s"' % (typo, type(value))
    if hasattr(typo, '__origin__'):
        if not isinstance(value, typo.__origin__):
            return False, 'expected "%s", got "%s"' % (typo, type(value))
        if typo.__args__:
            if len(typo.__args__) == 1:
                for i in value:
                    if not (res := check_type(i, typo.__args__))[0]:
                        return res
            elif len(typo.__args__) != len(value):
                return False, 'expected "%s", got "%s"' % (typo, str(value))
            else:
                for i in range(len(value)):
                    if not (res := check_type(value[i], typo.__args__[i]))[0]:
                        return res
    return True, None


def check_dict(value: T, typo: Any) -> CheckerType:
    if isinstance(typo, type) and not isinstance(value, typo):
        return False, 'expected "%s", got "%s"' % (typo, type(value))
    elif hasattr(typo, '__origin__'):
        if not isinstance(value, typo.__origin__):
            return False, 'expected "%s", got "%s"' % (typo, type(value))
        for i, j in value.items():
            if not (res := check_type(i, typo.__args__[0]))[0]:
                return False, 'key "%s", %s' % (i, res[1])
            if not (res := check_type(j, typo.__args__[1]))[0]:
                return False, 'value for key "%s", %s' % (i, res[1])
    return True, None


def check_callable(value: T, typo: Any) -> CheckerType:
    if not callable(value):
        return False, 'expected callable, got "%s"' % value
    if typo.__args__ and hasattr(value, '__annotations__'):
        for idx in range(value.__code__.co_argcount):
            if (var_name := value.__code__.co_varnames[idx]) in value.__annotations__:
                if not is_subtype(value.__annotations__[var_name], typo.__args__[idx]):
                    return (
                        False,
                        'arg "%s" is type of "%s", expected %s' % (
                            var_name,
                            value.__annotations__[var_name],
                            typo.__args__[idx],
                        ),
                    )
            if 'return' in value.__annotations__ and not is_subtype(value.__annotations__['return'], typo.__args__[-1]):
                return (
                    False,
                    'return value is type of "%s", expected %s' % (
                        value.__annotations__['return'],
                        typo.__args__[idx],
                    ),
                )
    return True, None


def check_alias(attr: str) -> Callable[[T, Any], CheckerType]:
    return (
        lambda value, typo: (
            bool(getattr(value, attr, None)),
            'expected obj with method "%s()", got "%s"' % (attr, value),
        )
    )


SUPPORTED_TYPOS = {
    Optional: check_union,
    Union: check_union,
    List: check_list,
    list: check_list,
    Tuple: check_tuple,
    tuple: check_tuple,
    Dict: check_dict,
    dict: check_dict,
    Any: lambda *a, **b: (True, ''),
    abc.Callable: check_callable,
    abc.Iterable: check_alias('__iter__'),
    abc.Sized: check_alias('__len__'),
    abc.Hashable: check_alias('__hash__'),
    abc.Reversible: check_alias('__reversed__'),
    abc.Coroutine: lambda value, value_type: (asyncio.iscoroutine(value), 'Excpected Coroutine, got "%s"' % value),
    abc.Generator: (
        lambda value, value_type: (
            bool(getattr(value, '__next__', None) and getattr(value, 'send', None)),
            'Expected generator, got "%s"' % value,
        )
    ),
}  # type: Dict[Any, Callable[[T, Any], CheckerType]]

SUPPORTED_ALIASES = {
    callable: lambda *a, **b: (callable(a[0]), 'Expected callable obj, got "%s"' % a[0]),
}  # type: Dict[Any, Callable[[T, Any], CheckerType]]


def check_type(value: T, value_type: Any) -> CheckerType:
    if type(value_type) is tuple and len(value_type) == 1 and isinstance(value_type[0], type):
        value_type = value_type[0]
    if value_type in SUPPORTED_ALIASES:
        if not (res := SUPPORTED_ALIASES[value_type](value, value_type))[0]:
            return res
    if (
        (
            isinstance(value_type, type)
        ) or (
            (
                isinstance(value_type, tuple)
            ) and (
                all(isinstance(i, type) for i in value_type)
            )
        )
    ) and (
        not isinstance(value, value_type)
    ):
        return False, 'for "%s" expected type "%s", got "%s"' % (value, value_type, type(value))
    if hasattr(value_type, '__origin__'):
        if value_type.__origin__ in SUPPORTED_TYPOS:
            if not (res := SUPPORTED_TYPOS[value_type.__origin__](value, value_type))[0]:
                return res
    return True, None


def is_type(value: Any, type: Any) -> bool:
    return check_type(value, type)[0]


def staticclass(cls=None, /, strict: bool = True):
    def wrap(cls):
        def gen_init(ant: Dict[str, Any]) -> Callable[[Any], None]:
            def init(self, /, **kwargs) -> None:
                for arg_name, arg_type in ant.items():
                    if arg_name in kwargs:
                        if (res := check_type(kwargs[arg_name], arg_type))[0]:
                            setattr(self, arg_name, kwargs[arg_name])
                        else:
                            raise TypeError(res[1])
                    elif strict:
                        raise TypeError('arg "%s" not passed' % arg_name)
            return init
        ans = {}
        for _cls in cls.__mro__[::-1]:
            if hasattr(_cls, '__annotations__'):
                ans.update(_cls.__annotations__)

        setattr(cls, '__init__', gen_init(ans))
        return cls
    if cls:
        return wrap(cls)
    return wrap
