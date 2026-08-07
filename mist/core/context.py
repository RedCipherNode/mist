from __future__ import annotations

from dataclasses import dataclass, field

from mist.core.diagnostics import Diagnostics


@dataclass(slots=True)
class Context:
    """Shared execution context for a transformation pipeline."""

    diagnostics: Diagnostics = field(default_factory=Diagnostics)
