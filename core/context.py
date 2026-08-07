from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostics import Diagnostics


@dataclass(slots=True)
class Context:
    """Shared runtime state during a transformation pipeline."""

    diagnostics: Diagnostics = field(default_factory=Diagnostics)
