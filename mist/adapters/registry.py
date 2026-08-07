from __future__ import annotations

from pathlib import Path

from mist.adapters.adapter import Adapter


class AdapterRegistry:
    """Stores and resolves language adapters."""

    def __init__(self) -> None:
        self._adapters: list[Adapter] = []

    def register(self, adapter: Adapter) -> None:
        """Register a language adapter."""
        self._adapters.append(adapter)

    def unregister(self, adapter: Adapter) -> None:
        """Remove a registered adapter."""
        self._adapters.remove(adapter)

    def resolve(self, path: Path) -> Adapter | None:
        """Return the first adapter that supports the given path."""

        for adapter in self._adapters:
            if adapter.supports(path):
                return adapter

        return None

    @property
    def adapters(self) -> tuple[Adapter, ...]:
        """Registered adapters (read-only)."""
        return tuple(self._adapters)
