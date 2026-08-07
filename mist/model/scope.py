from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Scope:
    id: int

    parent: "Scope | None" = None

    children: list["Scope"] = field(default_factory=list)

    symbols: list = field(default_factory=list)
