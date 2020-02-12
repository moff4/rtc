
# STC - Static Type Checker

Runtime type checker

## example:

```python

from typing import Any, Callable, List, Dict, Optional

from stc import staticclass

@staticclass
class A:
    a: int
    f: Optional[Callable[[List[str]], Dict[str, Any]]]

def f(strs: List[str]) -> Dict[str, Any]:
    return {k: idx for idx, st in enumerate(strs) for k in st}

def g(strs: List[str]) -> None:
    return

A(a=1, f=f)  # ok
A(a='some-str', f=f)  # raise TypeError as str != itn
A(a=123, f=g)  # raise TypeError as g returns wrong type

```