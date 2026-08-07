from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from mist.core.base_pass import BasePass


class Pipeline:
    """Executes transformation passes sequentially."""

    def __init__(self) -> None:
        self._passes: list[BasePass] = []

    def add(self, transform: BasePass) -> None:
        """Register a transformation pass."""
        self._passes.append(transform)

    def extend(self, transforms: Iterable[BasePass]) -> None:
        """Register multiple transformation passes."""
        self._passes.extend(transforms)

    def clear(self) -> None:
        """Remove all registered passes."""
        self._passes.clear()

    def run(self, tree: Any, context: Any) -> Any:
        """Execute all registered passes."""

        current = tree

        for transform in self._passes:
            current = transform.apply(current, context)

        return current

    @property
    def passes(self) -> tuple[BasePass, ...]:
        """Registered transformation passes."""
        return tuple(self._passes)
