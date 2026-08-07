from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Adapter(ABC):
    """Base contract for language adapters."""

    @property
    @abstractmethod
    def language(self) -> str:
        """Language identifier."""
        ...

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """Return True if this adapter supports the given path."""
        ...

    @abstractmethod
    def parse(self, source: str) -> Any:
        """Parse source code into an internal representation."""
        ...

    @abstractmethod
    def emit(self, tree: Any) -> str:
        """Convert an internal representation back into source code."""
        ...
