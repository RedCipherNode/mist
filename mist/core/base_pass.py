from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BasePass(ABC):
    """Base class for all transformation passes."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique pass name."""
        ...

    @abstractmethod
    def apply(self, tree: Any, context: Any) -> Any:
        """
        Apply the transformation.

        Parameters
        ----------
        tree:
            Language-specific syntax tree.

        context:
            Shared pipeline execution context.

        Returns
        -------
        Any
            The transformed syntax tree.
        """
        ...
