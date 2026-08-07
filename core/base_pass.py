from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BasePass(ABC):
    """Base class for every transformation pass."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable pass name."""
        raise NotImplementedError

    @abstractmethod
    def run(self, tree: Any, context: Any) -> Any:
        """
        Execute the transformation.

        Parameters
        ----------
        tree:
            Language-specific syntax tree.

        context:
            Shared runtime context.

        Returns
        -------
        The transformed tree.
        """
        raise NotImplementedError
