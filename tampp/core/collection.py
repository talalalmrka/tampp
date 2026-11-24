from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Collection(Generic[T]):
    def __init__(self, items: dict[str, T] | list[T] | None = None):
        self._items: dict[str, T] = {}

        if isinstance(items, dict):
            self._items = items.copy()
        elif isinstance(items, list):
            self._items = dict(enumerate(items))

    def all(self) -> dict[str, T]:
        return self._items.copy()

    def get(self, key: str | int, default: Any = None) -> T | Any:
        return self._items.get(key, default)

    def set(self, key: str | int, value: T) -> Collection[T]:
        self._items[key] = value
        return self

    def has(self, key: str | int) -> bool:
        return key in self._items

    def remove(self, key: str | int) -> Collection[T]:
        self._items.pop(key, None)
        return self

    def keys(self) -> list:
        return list(self._items.keys())

    def values(self) -> list[T]:
        return list(self._items.values())

    def items(self):
        return self._items.items()

    def first(self, default: Any = None) -> T | Any:
        return next(iter(self._items.values()), default)

    def last(self, default: Any = None) -> T | Any:
        return next(reversed(self._items.values()), default)

    def filter(self, callback: Callable[[T, Any], bool]) -> Collection[T]:
        return Collection(
            {key: value for key, value in self._items.items() if callback(value, key)}
        )

    def map(self, callback: Callable[[T, Any], Any]) -> Collection:
        return Collection(
            {key: callback(value, key) for key, value in self._items.items()}
        )

    def find(self, callback: Callable[[T, Any], bool], default=None):
        for key, value in self._items.items():
            if callback(value, key):
                return value
        return default

    def contains(self, value: T) -> bool:
        return value in self._items.values()

    def count(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return not self._items

    def to_list(self) -> list[T]:
        return list(self._items.values())

    def to_dict(self) -> dict:
        return self._items.copy()

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value

    def __contains__(self, key):
        return key in self._items

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Collection({self._items!r})"
