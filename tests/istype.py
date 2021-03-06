
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
    Generator,
    TypedDict,
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

    def test_generator(self):
        def f():
            x = yield  # type: int
            while x > 0:
                yield x

        self.assertFalse(is_type(range(10), Generator))
        self.assertFalse(is_type(map(int, [1, 2, 3]), Generator))
        self.assertTrue(is_type(f(), Generator))

    def test_typeddict(self):
        class A(TypedDict):
            a: int
            b: str

        class B(TypedDict):
            a: Union[int, float]
            b: Optional[str]

        class C(TypedDict, total=False):
            a: Union[int, float]
            b: Optional[str]

        self.assertTrue(is_type({'a': 123, 'b': '123'}, A))
        self.assertFalse(is_type({'a': 123, 'b': None}, A))
        self.assertFalse(is_type({'a': 12.3, 'b': '123'}, A))
        self.assertTrue(is_type({'a': 12.3, 'b': '123'}, B))
        self.assertTrue(is_type({'a': 123, 'b': None}, B))
        self.assertTrue(is_type({'a': 12.3, 'b': '123'}, B))
        self.assertTrue(is_type({'a': 12.3, 'b': None}, B))
        self.assertFalse(is_type({'b': None}, B))
        self.assertFalse(is_type({'a': 123}, B))
        self.assertFalse(is_type({'a': 'None'}, B))
        self.assertFalse(is_type({'b': 'None'}, B))
        self.assertTrue(is_type({'a': 12.3, 'b': '123'}, C))
        self.assertTrue(is_type({'a': 123, 'b': None}, C))
        self.assertTrue(is_type({'a': 12.3, 'b': '123'}, C))
        self.assertTrue(is_type({'a': 12.3, 'b': None}, C))
        self.assertTrue(is_type({'b': None}, C))
        self.assertFalse(is_type({'a': 'None'}, C))
        self.assertTrue(is_type({'a': 123}, C))

    def test_schema_schek(self):
        class TextData(TypedDict):
            text: Optional[str]

        class WeatherData(TypedDict):
            time: int
            loaction: Dict[str, float]
            exrta: Optional[str]

        class Object(TypedDict):
            object_id: str
            data: Union[TextData, WeatherData]

        class Action(TypedDict, total=False):
            action_id: str
            title: str
            color: Optional[str]
            handable: bool

        class Session(TypedDict, total=False):
            session_id: str
            message_id: int
            time_zone: Optional[str]

        class Response(TypedDict):
            objects: List[Object]
            actions: List[Action]
            session: Session

        self.assertTrue(
            is_type(
                {
                    'actions': [
                        {
                            'action_id': 'some-id',
                            'title': 'ok',
                            'color': None,
                            'handable': True,
                        }
                    ],
                    'objects': [],
                    'session': {
                        'session_id': '-some-id-',
                        'message_id': 0,
                    }
                },
                Response,
            )
        )
        self.assertTrue(
            is_type(
                {
                    'actions': [],
                    'objects': [
                        {
                            'object_id': 'text',
                            'data': {
                                'text': None,
                            }
                        }
                    ],
                    'session': {
                        'session_id': '-some-id-',
                        'message_id': 0,
                    }
                },
                Response,
            )
        )
        self.assertFalse(
            is_type(
                {
                    'actions': [],
                    'objects': [
                        {
                            'object_id': 'text',
                            'data': {}
                        }
                    ],
                    'session': {
                        'session_id': '-some-id-',
                        'message_id': 0,
                    }
                },
                Response,
            )
        )
