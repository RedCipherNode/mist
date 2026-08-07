from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Adapter(ABC):
    """Base contract for every language adapter."""

    @property
    @abstractmethod
    def language(self) -> str:
        """Language name."""
        raise NotImplementedError

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """Return True if this adapter supports the file."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, source: str) -> Any:
        """Parse source code into a language tree."""
        raise NotImplementedError

    @abstractmethod
    def emit(self, tree: Any) -> str:
        """Convert the language tree back into source code."""
        raise NotImplementedError
