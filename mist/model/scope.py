from __future__ import annotations

from dataclasses import dataclass, field

from mist.model.symbol import Symbol


@dataclass(slots=True)
class Scope:
    name: str

    parent: "Scope | None" = None

    symbols: dict[str, Symbol] = field(default_factory=dict)
