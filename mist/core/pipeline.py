from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from mist.core.pass import Pass


class Pipeline:
    """Executes transformation passes sequentially."""

    def __init__(self) -> None:
        self._passes: list[Pass] = []

    def add(self, transform: Pass) -> None:
        """Register a transformation pass."""
        self._passes.append(transform)

    def extend(self, transforms: Iterable[Pass]) -> None:
        """Register multiple transformation passes."""
        self._passes.extend(transforms)

    def clear(self) -> None:
        """Remove all registered passes."""
        self._passes.clear()

    def run(self, tree: Any, context: Any) -> Any:
        """Execute every registered pass."""

        current = tree

        for transform in self._passes:
            current = transform.run(current, context)

        return current

    @property
    def passes(self) -> tuple[Pass, ...]:
        """Registered passes (read-only)."""
        return tuple(self._passes)