from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def given(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
def settings(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
