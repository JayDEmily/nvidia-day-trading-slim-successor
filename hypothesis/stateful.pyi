from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

class RuleBasedStateMachine:
    TestCase: type[object]

def initialize(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
def rule(*args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
