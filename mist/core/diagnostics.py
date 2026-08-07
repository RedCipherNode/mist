from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass(slots=True, frozen=True)
class Diagnostic:
    severity: Severity
    message: str


class Diagnostics:
    def __init__(self) -> None:
        self._items: list[Diagnostic] = []

    def info(self, message: str) -> None:
        self._items.append(Diagnostic(Severity.INFO, message))

    def warning(self, message: str) -> None:
        self._items.append(Diagnostic(Severity.WARNING, message))

    def error(self, message: str) -> None:
        self._items.append(Diagnostic(Severity.ERROR, message))

    @property
    def items(self) -> tuple[Diagnostic, ...]:
        return tuple(self._items)

    def clear(self) -> None:
        self._items.clear()
