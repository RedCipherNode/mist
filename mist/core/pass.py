from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Pass(ABC):
    """Base contract for every transformation pass."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the pass name."""
        ...

    @abstractmethod
    def run(self, tree: Any, context: Any) -> Any:
        """
        Execute the transformation.

        Parameters
        ----------
        tree:
            Transformation target.

        context:
            Shared execution context.

        Returns
        -------
        The transformed tree.
        """
        ...
