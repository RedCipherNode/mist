from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from mist.model import Symbol


class Adapter(ABC):
    """Language adapter."""

    @abstractmethod
    def parse(self, source: str) -> Any: ...

    @abstractmethod
    def collect_symbols(self, tree: Any) -> list[Symbol]: ...

    @abstractmethod
    def rewrite(self, tree: Any, symbols: list[Symbol]) -> Any: ...

    @abstractmethod
    def emit(self, tree: Any) -> str: ...
