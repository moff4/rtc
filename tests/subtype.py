

from typing import List, Dict, Tuple, Union, Optional, Any, Callable
from unittest import TestCase

from stc import is_subtype


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
        self.assertFalse(is_subtype(Tuple[Any], Tuple[str]))
        self.assertFalse(is_subtype(Tuple[int], Tuple[str]))

    def test_dict(self):
        self.assertTrue(is_subtype(dict, Dict))
        self.assertTrue(is_subtype(dict, Dict[str, str]))
        self.assertFalse(is_subtype(Dict, Dict[str, str]))
        self.assertTrue(is_subtype(Dict[str, str], Dict))
        self.assertTrue(is_subtype(Dict[str, str], Dict[str, Any]))
        self.assertFalse(is_subtype(Dict[str, Any], Dict[str, str]))
        self.assertTrue(is_subtype(Dict[str, str], Dict[Union[str, int], str]))
        self.assertTrue(is_subtype(Dict[int, str], Dict[Union[str, int], str]))

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
