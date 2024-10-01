from dataclasses import dataclass
from typing import Callable, Any, Iterable

@dataclass
class AddAccumulator:
    name: str
    initial_value: Any

@dataclass
class AddIterable:
    name: str
    iterable: Iterable

@dataclass
class SetFilter:
    filter_function: Callable[..., bool]

@dataclass
class SetResult:
    result_name: str

@dataclass
class SetBody:
    body_function: Callable[..., Any]
