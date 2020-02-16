from typing import (
    List,
    Dict,
    Set,
    Tuple,
    Union,
    Optional,
    Any,
    Callable,
    Iterable,
    Hashable,
    Sized,
    Container,
    Reversible,
    Generator,
    Coroutine,
    AsyncGenerator,
    Generic,
    TypeVar,
)
from unittest import TestCase

from rtc import is_subtype


class TestSubType(TestCase):

    def test_simple(self):
        self.assertTrue(is_subtype(bool, int))
        self.assertTrue(is_subtype(bool, bool))
        self.assertTrue(is_subtype(int, int))
        self.assertFalse(is_subtype(int, bool))
        self.assertTrue(is_subtype(type('new_class', (list,), {}), list))
        self.assertFalse(is_subtype(list, type('new_class', (list,), {})))

    def test_any(self):
        self.assertTrue(is_subtype(int, Any))
        self.assertTrue(is_subtype(float, Any))
        self.assertTrue(is_subtype('anything', Any))
        self.assertFalse(is_subtype(Any, int))
        self.assertFalse(is_subtype(Any, float))
        self.assertFalse(is_subtype(Any, str))

    def test_optional(self):
        self.assertTrue(is_subtype(int, Optional[int]))
        self.assertTrue(is_subtype(type(None), Optional[int]))
        self.assertFalse(is_subtype(str, Optional[int]))
        self.assertTrue(is_subtype(Optional[int], Optional[int]))
        self.assertTrue(Optional[str], Union[str, int, None])
        self.assertFalse(is_subtype(Union[str, int, None], Optional[str]))

    def test_union(self):
        self.assertTrue(is_subtype(int, Union[int, float]))
        self.assertTrue(is_subtype(type(None), Union[int, type(None)]))
        self.assertTrue(is_subtype(Union[int, float], Union[int, float, str]))
        self.assertTrue(is_subtype(Union[int, float, str], Union[int, float, str]))
        self.assertFalse(is_subtype(Union[int, float, str], Union[int, float]))
        self.assertFalse(is_subtype(str, Union[int, float, None]))

    def test_list(self):
        self.assertTrue(is_subtype(list, List))
        self.assertTrue(is_subtype(List, list))
        self.assertTrue(is_subtype(List, List))
        self.assertTrue(is_subtype(List[str], List))
        self.assertFalse(is_subtype(List, List[str]))
        self.assertFalse(is_subtype(int, List))
        self.assertFalse(is_subtype(int, List[str]))
        self.assertTrue(is_subtype(List[str], List[Any]))
        self.assertFalse(is_subtype(List[Any], List[str]))
        self.assertFalse(is_subtype(List[int], List[str]))

    def test_tuple(self):
        self.assertTrue(is_subtype(tuple, Tuple))
        self.assertTrue(is_subtype(Tuple, tuple))
        self.assertTrue(is_subtype(Tuple, Tuple))
        self.assertTrue(is_subtype(Tuple[str], Tuple))
        self.assertFalse(is_subtype(Tuple, Tuple[str]))
        self.assertFalse(is_subtype(int, Tuple))
        self.assertFalse(is_subtype(int, Tuple[str]))
        self.assertTrue(is_subtype(Tuple[str], Tuple[Any]))
        self.assertTrue(is_subtype(Tuple[str, str], Tuple[Any]))
        self.assertTrue(is_subtype(Tuple[str, str], Tuple[str]))
        self.assertTrue(is_subtype(Tuple[str, str], Tuple[str, str]))
        self.assertFalse(is_subtype(Tuple[str, str], Tuple[str, int]))
        self.assertFalse(is_subtype(Tuple[str, int, str], Tuple[str, int]))
        self.assertFalse(is_subtype(Tuple[Any], Tuple[str]))
        self.assertFalse(is_subtype(Tuple[int], Tuple[str]))

    def test_set(self):
        self.assertTrue(is_subtype(set, Set))
        self.assertTrue(is_subtype(Set, set))
        self.assertTrue(is_subtype(Set, Set))
        self.assertTrue(is_subtype(Set[str], Set))
        self.assertFalse(is_subtype(Set, Set[str]))
        self.assertFalse(is_subtype(int, Set))
        self.assertFalse(is_subtype(int, Set[str]))
        self.assertTrue(is_subtype(Set[str], Set[Any]))
        self.assertFalse(is_subtype(Set[Any], Set[str]))
        self.assertFalse(is_subtype(Set[int], Set[str]))

    def test_dict(self):
        self.assertTrue(is_subtype(dict, Dict))
        self.assertTrue(is_subtype(dict, Dict[str, str]))
        self.assertFalse(is_subtype(Dict, Dict[str, str]))
        self.assertTrue(is_subtype(Dict[str, str], Dict))
        self.assertTrue(is_subtype(Dict[str, str], Dict[str, Any]))
        self.assertFalse(is_subtype(Dict[str, Any], Dict[str, str]))
        self.assertTrue(is_subtype(Dict[str, str], Dict[Union[str, int], str]))
        self.assertTrue(is_subtype(Dict[int, str], Dict[Union[str, int], str]))
        self.assertTrue(
            is_subtype(
                Dict[str, List[Union[str, type(None)]]],
                Dict[Any, List[Union[str, type(None)]]],
            )
        )

    def test_callable(self):
        self.assertTrue(is_subtype(Callable, Callable))
        self.assertTrue(is_subtype(Callable[[int, str], None], Callable[[int, str], None]))
        self.assertTrue(is_subtype(Callable[[int, str], None], Callable[[Any, str], None]))
        self.assertTrue(is_subtype(Callable[[int, str], None], Callable[[Any, Any], Any]))
        self.assertTrue(is_subtype(Callable[[int, str], None], Callable[[Any, str], Any]))
        self.assertTrue(is_subtype(Callable[[int, str], None], Callable[[Any, Any], None]))
        self.assertTrue(is_subtype(Callable[[int, str], int], Callable[[Union[int, float], str], Any]))
        self.assertTrue(is_subtype(Callable[[Any, str], Any], Callable[[Any, str], Any]))
        self.assertTrue(is_subtype(Callable[[int, Any], Any], Callable[[Any, Any], Any]))
        self.assertTrue(is_subtype(Callable[[int, Any], None], Callable[[int, Any], Any]))
        self.assertTrue(is_subtype(Callable[[Any, str], None], Callable[[Any, str], None]))
        self.assertFalse(is_subtype(Callable[[Any, Any], Any], Callable[[Union[int, float], str], Any]))
        self.assertFalse(is_subtype(Callable[[Any, float], str], Callable[[int, float], str]))

    def test_iterable(self):
        self.assertTrue(is_subtype(list, Iterable))
        self.assertTrue(is_subtype(dict, Iterable))
        self.assertTrue(is_subtype(tuple, Iterable))
        self.assertFalse(is_subtype(int, Iterable))
        self.assertFalse(is_subtype(float, Iterable))

        self.assertTrue(is_subtype(List, Iterable))
        self.assertTrue(is_subtype(List[Any], Iterable))
        self.assertTrue(is_subtype(List[str], Iterable[str]))
        self.assertTrue(is_subtype(List[Any], Iterable[Any]))
        self.assertTrue(is_subtype(List[str], Iterable[Any]))
        self.assertFalse(is_subtype(List[int], Iterable[str]))

        self.assertTrue(is_subtype(Tuple, Iterable))
        self.assertTrue(is_subtype(Tuple[Any], Iterable[Any]))
        self.assertTrue(is_subtype(Tuple[Any], Iterable))
        self.assertTrue(is_subtype(Tuple[str], Iterable[str]))
        self.assertTrue(is_subtype(Tuple[str], Iterable[Any]))
        self.assertFalse(is_subtype(Tuple[int], Iterable[str]))

        self.assertTrue(is_subtype(Dict, Iterable))
        self.assertTrue(is_subtype(Dict[Any, Any], Iterable))
        self.assertTrue(is_subtype(Dict[Any, str], Iterable[Any]))
        self.assertTrue(is_subtype(Dict[str, float], Iterable[str]))
        self.assertTrue(is_subtype(Dict[str, int], Iterable[Any]))
        self.assertFalse(is_subtype(Dict[int, str], Iterable[str]))

        self.assertTrue(is_subtype(Iterable, Iterable))
        self.assertTrue(is_subtype(Iterable, Iterable[Any]))
        self.assertTrue(is_subtype(Iterable[Any], Iterable[Any]))
        self.assertTrue(is_subtype(Iterable[int], Iterable[Any]))
        self.assertTrue(is_subtype(Iterable[int], Iterable[Union[str, int]]))
        self.assertFalse(is_subtype(Iterable[int], Iterable[str]))

        self.assertTrue(is_subtype(set, Iterable))
        self.assertTrue(is_subtype(Set, Iterable))
        self.assertTrue(is_subtype(Set[Any], Iterable[Any]))
        self.assertTrue(is_subtype(Set[int], Iterable[Any]))
        self.assertTrue(is_subtype(Set[int], Iterable[Union[str, int]]))
        self.assertFalse(is_subtype(Set[int], Iterable[str]))

    def test_hashable(self):
        self.assertFalse(is_subtype(list, Hashable))
        self.assertFalse(is_subtype(List, Hashable))
        self.assertFalse(is_subtype(List[str], Hashable))
        self.assertFalse(is_subtype(dict, Hashable))
        self.assertFalse(is_subtype(Dict, Hashable))
        self.assertFalse(is_subtype(Dict[str, Any], Hashable))
        self.assertFalse(is_subtype(set, Hashable))
        self.assertFalse(is_subtype(Set, Hashable))
        self.assertFalse(is_subtype(Set[bool], Hashable))
        self.assertTrue(is_subtype(tuple, Hashable))
        self.assertTrue(is_subtype(Tuple, Hashable))
        self.assertTrue(is_subtype(Tuple[str], Hashable))
        self.assertTrue(is_subtype(Tuple[str, int], Hashable))
        self.assertTrue(is_subtype(int, Hashable))
        self.assertTrue(is_subtype(str, Hashable))
        self.assertTrue(is_subtype(float, Hashable))
        self.assertTrue(is_subtype(Callable[[int, int], List[str]], Hashable))
        self.assertTrue(is_subtype(Union[tuple, str], Hashable))
        self.assertFalse(is_subtype(Union[dict, Tuple[int]], Hashable))
        self.assertFalse(is_subtype(Union[Dict[str, Any], float], Hashable))

    def test_sized(self):
        self.assertFalse(is_subtype(int, Sized))
        self.assertFalse(is_subtype(Any, Sized))
        self.assertFalse(is_subtype(float, Sized))
        self.assertTrue(is_subtype(str, Sized))
        self.assertTrue(is_subtype(list, Sized))
        self.assertTrue(is_subtype(List, Sized))
        self.assertTrue(is_subtype(List[str], Sized))
        self.assertTrue(is_subtype(tuple, Sized))
        self.assertTrue(is_subtype(Tuple, Sized))
        self.assertTrue(is_subtype(Tuple[Any], Sized))
        self.assertTrue(is_subtype(dict, Sized))
        self.assertTrue(is_subtype(Dict, Sized))
        self.assertTrue(is_subtype(Dict[int, float], Sized))
        self.assertTrue(is_subtype(set, Sized))
        self.assertTrue(is_subtype(Set, Sized))
        self.assertTrue(is_subtype(Set[int], Sized))
        self.assertTrue(is_subtype(Union[set, List[int]], Sized))
        self.assertFalse(is_subtype(Union[int, List[int]], Sized))
        self.assertFalse(is_subtype(Union[int, float], Sized))

    def test_contains(self):
        self.assertFalse(is_subtype(int, Container))
        self.assertFalse(is_subtype(float, Container))
        self.assertFalse(is_subtype(bool, Container))
        self.assertFalse(is_subtype(Callable, Container))
        self.assertTrue(is_subtype(dict, Container))
        self.assertTrue(is_subtype(Dict, Container))
        self.assertTrue(is_subtype(Dict[str, Any], Container))
        self.assertTrue(is_subtype(Dict[str, int], Container))
        self.assertTrue(is_subtype(list, Container))
        self.assertTrue(is_subtype(List, Container))
        self.assertTrue(is_subtype(List[str], Container))
        self.assertTrue(is_subtype(List[Any], Container))
        self.assertTrue(is_subtype(tuple, Container))
        self.assertTrue(is_subtype(Tuple, Container))
        self.assertTrue(is_subtype(Tuple[Any], Container))
        self.assertTrue(is_subtype(Tuple[float], Container))
        self.assertTrue(is_subtype(set, Container))
        self.assertTrue(is_subtype(Set, Container))
        self.assertTrue(is_subtype(Set[Union[float, int]], Container))
        self.assertFalse(is_subtype(Union[float, int], Container))
        self.assertFalse(is_subtype(Union[float, Dict], Container))
        self.assertTrue(is_subtype(Union[list, Set[int]], Container))

    def test_reversible(self):
        self.assertFalse(is_subtype(int, Reversible))
        self.assertFalse(is_subtype(float, Reversible))
        self.assertFalse(is_subtype(bool, Reversible))
        self.assertFalse(is_subtype(Callable, Reversible))
        self.assertTrue(is_subtype(str, Reversible))
        self.assertTrue(is_subtype(list, Reversible))
        self.assertTrue(is_subtype(List, Reversible))
        self.assertTrue(is_subtype(List[int], Reversible))
        self.assertTrue(is_subtype(dict, Reversible))
        self.assertTrue(is_subtype(Dict, Reversible))
        self.assertTrue(is_subtype(Dict[str, Any], Reversible))
        self.assertFalse(is_subtype(set, Reversible))
        self.assertFalse(is_subtype(Set, Reversible))
        self.assertFalse(is_subtype(Set[int], Reversible))
        self.assertTrue(is_subtype(tuple, Reversible))
        self.assertTrue(is_subtype(Tuple, Reversible))
        self.assertTrue(is_subtype(Tuple[int], Reversible))
        self.assertTrue(is_subtype(Tuple[str], Reversible))
        self.assertTrue(is_subtype(Tuple[str, int], Reversible))

    def test_corotine(self):
        self.assertTrue(is_subtype(Coroutine, Coroutine))
        self.assertTrue(is_subtype(Coroutine, Coroutine[Any, Any, Any]))
        self.assertTrue(is_subtype(Coroutine[Any, Any, Any], Coroutine[Any, Any, Any]))
        self.assertTrue(is_subtype(Coroutine[Any, Any, Any], Coroutine))
        self.assertTrue(is_subtype(Coroutine[int, Any, Any], Coroutine[Union[int, float], Any, Any]))
        self.assertFalse(is_subtype(Coroutine[int, Any, Any], Coroutine[Optional[float], Any, Any]))

    def test_generator(self):
        self.assertTrue(is_subtype(Generator, Generator))
        self.assertTrue(is_subtype(Generator, Generator[Any, Any, Any]))
        self.assertTrue(is_subtype(Generator[Any, Any, Any], Generator[Any, Any, Any]))
        self.assertTrue(is_subtype(Generator[Any, Any, Any], Generator))
        self.assertTrue(is_subtype(Generator[int, Any, Any], Generator[Union[int, float], Any, Any]))
        self.assertFalse(is_subtype(Generator[int, Any, Any], Generator[Optional[float], Any, Any]))

    def test_async_generator(self):
        self.assertTrue(is_subtype(AsyncGenerator, AsyncGenerator))
        self.assertTrue(is_subtype(AsyncGenerator, AsyncGenerator[Any, Any]))
        self.assertTrue(is_subtype(AsyncGenerator[Any, Any], AsyncGenerator[Any, Any]))
        self.assertTrue(is_subtype(AsyncGenerator[Any, Any], AsyncGenerator))
        self.assertTrue(is_subtype(AsyncGenerator[int, Any], AsyncGenerator[Union[int, float], Any]))
        self.assertFalse(is_subtype(AsyncGenerator[int, Any], AsyncGenerator[Optional[float], Any]))

    def test_generic(self):
        K = TypeVar('K')
        V = TypeVar('V')

        class A(Generic[K, V]):
            ...

        self.assertTrue(is_subtype(A, A))
        self.assertTrue(is_subtype(A[str, str], A[Any, Any]))
        self.assertTrue(is_subtype(A[str, str], A[Any, Any]))
        self.assertFalse(is_subtype(A[str, Any], A[Any, str]))