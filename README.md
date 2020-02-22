
# RTC - Runtime Type Checker

[![Build Status](https://travis-ci.org/moff4/rtc.svg?branch=master)](https://travis-ci.org/moff4/rtc)
[![CodeFactor](https://www.codefactor.io/repository/github/moff4/rtc/badge)](https://www.codefactor.io/repository/github/moff4/rtc)


## Example of usage:

### type cheker
```python

from typing import List, Dict, Any, Union, Optional

from rtc import is_type

print(is_type(123, Optional[int]))  # True
print(is_type([1, 2, 123.123], List[Union[int, float]])) # True
print(is_type({1: 2}, Dict[str, int]))  # False

```

### subtype cheker
```python

from typing import Any, Union, List, Dict, Optional

from rtc import is_subtype

print(is_subtype(List[str], List[Any]))  # True
print(is_subtype(Dict[str, Optional[float]], Dict[str, Union[int, float, None]])  # True
print(is_subtype(Union[int, float], float))  # False
```

### Schema cheker

```python
from typing import List, Dict, Optional, Union, TypedDict
from rtc import is_type

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

is_type(
    {
        'actions': [{'action_id': 'some-id', 'title': 'ok', 'color': None, 'handable': True}],
        'objects': [],
        'session': {'session_id': '-some-id-', 'message_id': 0}
    },
    Response,
)  # return True
is_type(
    {
        'actions': [],
        'objects': [{'object_id': 'text', 'data': {}}],
        'session': {'session_id': '-some-id-', 'message_id': 0},
    },
    Response,
)  # return False as Object.data is invalid 
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