from typing import Any, Callable, ParamSpec, TypeVar
from . import strategies

P = ParamSpec("P")
R = TypeVar("R")

def given(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
def settings(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
