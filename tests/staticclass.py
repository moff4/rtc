
from typing import List, Dict, Tuple, Union, Optional, Any, Callable
from unittest import TestCase

from rtc import staticclass


class TestStaticClass(TestCase):

    def test_simple_ok(self):
        @staticclass(strict=False)
        class A:
            a: int
            b: float

        self.assertTrue(bool(A()))
        self.assertTrue(bool(A(a=1)))
        self.assertTrue(bool(A(b=1.1)))
        self.assertTrue(bool(A(a=123, b=11.196)))

    def test_simple_fail(self):
        @staticclass(strict=False)
        class A:
            a: int
            b: float

        self.assertRaises(TypeError, A, a='1')
        self.assertRaises(TypeError, A, b='1.1')
        self.assertRaises(TypeError, A, a='1', b=1.1)
        self.assertRaises(TypeError, A, a=1, b='1.1')

    def test_strict(self):
        @staticclass
        class A:
            a: int
            b: float

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, b=1.1)
        self.assertTrue(bool(A(a=123, b=11.196)))

    def test_typing_list_1(self):
        @staticclass
        class A:
            a: List

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, b=1.1)
        self.assertTrue(bool(A(a=[123])))
        self.assertTrue(bool(A(a=[123, '123'])))

    def test_typing_list_2(self):
        @staticclass
        class A:
            a: List[int]

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertTrue(bool(A(a=[123])))
        self.assertRaises(TypeError, A, a=[123, '123'])

    def test_typing_tuple_1(self):
        @staticclass
        class A:
            a: Tuple

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, b=1.1)
        self.assertTrue(bool(A(a=(123,))))
        self.assertTrue(bool(A(a=(123, '123'))))

    def test_typing_tuple_2(self):
        @staticclass
        class A:
            a: Tuple[int]

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertTrue(bool(A(a=(123,))))
        self.assertRaises(TypeError, A, a=(123, '123'))

    def test_typing_dict_1(self):
        @staticclass
        class A:
            a: Dict

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, b=1.1)
        self.assertTrue(bool(A(a={1: 2, 1.1: '123'})))
        self.assertTrue(bool(A(a={123: '123', '123': 123})))

    def test_typing_dict_2(self):
        @staticclass
        class A:
            a: Dict[str, int]

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertTrue(bool(A(a={'123': 123, 'abc': 111})))
        self.assertRaises(TypeError, A, a={123: '123'})
        self.assertRaises(TypeError, A, a={12.3: 123})
        self.assertRaises(TypeError, A, a={'12.3': 12.3})

    def test_any(self):
        @staticclass
        class A:
            a: Any

        self.assertTrue(bool(A(a=1)))
        self.assertTrue(bool(A(a=12.3)))
        self.assertTrue(bool(A(a=None)))
        self.assertTrue(bool(A(a='None')))

    def test_optional(self):
        @staticclass
        class A:
            a: Optional[str]

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertTrue(bool(A(a=None)))
        self.assertTrue(bool(A(a='None')))

    def test_union(self):
        @staticclass
        class A:
            a: Union[str, int]

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=None)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertTrue(bool(A(a=1)))
        self.assertTrue(bool(A(a='None')))

    def test_callable_1(self):
        @staticclass
        class A:
            a: callable

        def f(x):
            return x

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=None)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertRaises(TypeError, A, a='1.1')
        self.assertRaises(TypeError, A, a=['1.1'])
        self.assertTrue(bool(A(a=f)))

    def test_callable_2(self):
        @staticclass
        class A:
            a: Callable

        def f(x):
            return x

        def g(x: int) -> int:
            return x

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=None)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a='1.1')
        self.assertRaises(TypeError, A, a=['1.1'])
        self.assertTrue(bool(A(a=f)))
        self.assertTrue(bool(A(a=g)))

    def test_callable_3(self):
        @staticclass
        class A:
            a: Callable[[int], int]

        def f(x):
            return x

        def g(x: int) -> int:
            return x

        def h(x: str) -> str:
            return x

        self.assertRaises(TypeError, A)
        self.assertRaises(TypeError, A, a=None)
        self.assertRaises(TypeError, A, a=1.1)
        self.assertRaises(TypeError, A, a='1.1')
        self.assertRaises(TypeError, A, a=1)
        self.assertRaises(TypeError, A, a=['1.1'])
        self.assertTrue(bool(A(a=f)))
        self.assertTrue(bool(A(a=g)))
        self.assertRaises(TypeError, A, a=h)
