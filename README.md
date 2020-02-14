
# RTC - Runtime Type Checker

[![Build Status](https://travis-ci.org/moff4/stc.svg?branch=master)](https://travis-ci.org/moff4/stc)
[![CodeFactor](https://www.codefactor.io/repository/github/moff4/stc/badge)](https://www.codefactor.io/repository/github/moff4/stc)


## example of usage:

### subtime cheker
```python

from typing import Any, Union, List, Dict, Optional

from rtc import is_subtype

print(is_subtype(List[str], List[Any]))  # True
print(is_subtype(Dict[str, Optional[float]], Dict[str, Union[int, float, None]])  # True
print(is_subtype(Union[int, float], float))  # False
```

### Class decorator
```python

from typing import Any, Callable, List, Dict, Optional

from rtc import staticclass

@staticclass
class A:
    a: int
    f: Optional[Callable[[List[str]], Dict[str, Any]]]

def f(strs: List[str]) -> Dict[str, Any]:
    return {k: idx for idx, st in enumerate(strs) for k in st}

def g(strs: List[str]) -> None:
    return

A(a=1, f=f)  # ok
A(a='some-str', f=f)  # raise TypeError as str != int
A(a=123, f=g)  # raise TypeError as g returns wrong type

```