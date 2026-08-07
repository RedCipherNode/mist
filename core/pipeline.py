from __future__ import annotations

from collections.abc import Iterable

from .pass import Pass


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

    def run(self, tree, context):
        """Execute all registered passes."""

        current = tree

        for transform in self._passes:
            current = transform.run(current, context)

        return current

    @property
    def passes(self) -> tuple[Pass, ...]:
        """Read-only registered passes."""
        return tuple(self._passes)