
from typing import (
    List,
    Dict,
    Tuple,
    Union,
    Optional,
    Any,
    Callable,
    Sized,
    Hashable,
    Reversible,
    Iterable,
    Coroutine,
)
from unittest import TestCase

from rtc import is_type


async def f(x: int) -> str:
    return str(x)


async def g(x: List[Optional[str]]) -> None:
    ...


class TestIsType(TestCase):

    def test_buidin(self):
        self.assertTrue(is_type(123, int))
        self.assertFalse(is_type(123.0, int))
        self.assertFalse(is_type('123.0', int))
        self.assertTrue(is_type('123', str))
        self.assertFalse(is_type([123], str))
        self.assertTrue(is_type(123.0, float))
        self.assertTrue(is_type({123: '123'}, dict))
        self.assertFalse(is_type({123: '123'}, float))

    def test_list(self):
        self.assertTrue(is_type([1, 2, 3], List))
        self.assertTrue(is_type([1, 2, 3], List[int]))
        self.assertFalse(is_type([1, 2, 3], List[str]))

    def test_tuple(self):
        self.assertTrue(is_type((1, 2, 3), Tuple))
        self.assertTrue(is_type((1, 2, 3), Tuple[Any]))
        self.assertTrue(is_type((1, '2', None), Tuple[Any]))
        self.assertTrue(is_type((1, 2, 3), Tuple[int]))
        self.assertTrue(is_type((1, '2'), Tuple[int, str]))
        self.assertFalse(is_type(('1', 2), Tuple[int, str]))
        self.assertFalse(is_type((1, 2, 3), Tuple[str]))

    def test_dict(self):
        self.assertTrue(is_type({'1': 123}, Dict))
        self.assertTrue(is_type({'1': 123}, Dict[str, int]))
        self.assertTrue(is_type({'1': 123}, Dict[str, Any]))
        self.assertTrue(is_type({'1': [123, None]}, Dict[str, Any]))
        self.assertTrue(is_type({('1', 11.1): 123}, Dict[Any, Any]))
        self.assertFalse(is_type({('1', 11.1): 123}, Dict[int, Any]))
        self.assertFalse(is_type({('1', 11.1): 123}, Dict[Any, str]))
        self.assertTrue(is_type({('1', 11.1): 123}, Dict[Any, Union[int, float]]))
        self.assertTrue(is_type({('1', 11.1): 12.3}, Dict[Any, Union[int, float]]))
        self.assertFalse(is_type({('1', 11.1): '12.3'}, Dict[Any, Union[int, float]]))

    def test_union(self):
        self.assertTrue(is_type(None, Optional[int]))
        self.assertTrue(is_type(123, Optional[int]))
        self.assertFalse(is_type(123.123, Optional[int]))
        self.assertFalse(is_type(123, Optional[float]))
        self.assertTrue(is_type(123, Union[int, float]))
        self.assertTrue(is_type(123.123, Union[int, float]))
        self.assertTrue(is_type(123.123, Union[int, float, None]))
        self.assertTrue(is_type(None, Union[int, float, None]))

    def test_callable(self):
        def f(x: int) -> None:
            ...
        self.assertTrue(is_type(f, Callable[[int], None]))
        self.assertTrue(is_type(f, Callable[[int], Any]))
        self.assertTrue(is_type(f, Callable[[Any], None]))
        self.assertTrue(is_type(f, Callable[[int], Optional[int]]))
        self.assertFalse(is_type(f, Callable[[str], None]))
        self.assertFalse(is_type(f, Callable[[int], int]))

        def g(x: Union[int, float], z: Dict[Any, List[Optional[str]]]) -> Union[bool, None]:
            ...

        self.assertFalse(is_type(g, Callable[[int, Dict], None]))
        self.assertFalse(is_type(g, Callable[[int, Dict], bool]))
        self.assertFalse(is_type(g, Callable[[int, Dict], Optional[bool]]))
        self.assertTrue(is_type(g, Callable[[Union[int, float], Dict], Optional[bool]]))
        self.assertFalse(is_type(g, Callable[[Union[int, float], Dict[str, List[str]]], Optional[bool]]))
        self.assertFalse(is_type(g, Callable[[Union[int, float], Dict[str, List[Optional[str]]]], Optional[bool]]))
        self.assertTrue(is_type(g, Callable[[Union[int, float], Dict[Any, List[Optional[str]]]], Optional[bool]]))

    def test_sized(self):
        self.assertFalse(is_type(123, Sized))
        self.assertFalse(is_type(12.3, Sized))
        self.assertFalse(is_type(Ellipsis, Sized))
        self.assertTrue(is_type('123', Sized))
        self.assertTrue(is_type(b'123', Sized))
        self.assertTrue(is_type(['123', '123'], Sized))
        self.assertTrue(is_type({'123', 123}, Sized))
        self.assertTrue(is_type({'123': 123}, Sized))
        self.assertTrue(is_type(('123', 123), Sized))

    def test_hashable(self):
        self.assertTrue(is_type(123, Hashable))
        self.assertTrue(is_type(12.3, Hashable))
        self.assertTrue(is_type(Ellipsis, Hashable))
        self.assertTrue(is_type('123', Hashable))
        self.assertTrue(is_type(b'123', Hashable))
        self.assertFalse(is_type(['123', '123'], Hashable))
        self.assertFalse(is_type({'123', 123}, Hashable))
        self.assertFalse(is_type({'123': 123}, Hashable))
        self.assertTrue(is_type(('123', 123), Hashable))

    def test_iterable(self):
        self.assertFalse(is_type(123, Iterable))
        self.assertFalse(is_type(12.3, Iterable))
        self.assertFalse(is_type(Ellipsis, Iterable))
        self.assertTrue(is_type('123', Iterable))
        self.assertTrue(is_type(b'123', Iterable))
        self.assertTrue(is_type(['123', '123'], Iterable))
        self.assertTrue(is_type({'123', 123}, Iterable))
        self.assertTrue(is_type({'123': 123}, Iterable))
        self.assertTrue(is_type(('123', 123), Iterable))
        self.assertTrue(is_type(range(10), Iterable))

    def test_reversed(self):
        self.assertFalse(is_type(123, Reversible))
        self.assertFalse(is_type(12.3, Reversible))
        self.assertFalse(is_type(Ellipsis, Reversible))
        self.assertFalse(is_type('123', Reversible))
        self.assertFalse(is_type(b'123', Reversible))
        self.assertTrue(is_type(['123', '123'], Reversible))
        self.assertFalse(is_type({'123', 123}, Reversible))
        self.assertTrue(is_type({'123': 123}, Reversible))
        self.assertFalse(is_type(('123', 123), Reversible))
        self.assertTrue(is_type(range(10), Reversible))

    def test_coroutine(self):
        self.assertTrue(is_type(f(123), Coroutine))
        self.assertFalse(is_type(f, Coroutine))
        self.assertTrue(is_type(g('aaa'), Coroutine))
        self.assertFalse(is_type(g, Coroutine))
        self.assertFalse(is_type(123, Coroutine))
        self.assertFalse(is_type(lambda x: x, Coroutine))
        self.assertFalse(is_type('smth', Coroutine))
        self.assertFalse(is_type([123, 12.11], Coroutine))
