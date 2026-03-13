from typing import Any, Callable, TypeVar, get_args

F = TypeVar("F", bound=Callable[..., Any])


def override(func: F) -> F:
    return func


def enum_to_items(type: Any) -> list[tuple[str, str, str]]:
    return [(t, t.replace("_", " ").title(), "") for t in get_args(type)]
