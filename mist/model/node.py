from __future__ import annotations

from dataclasses import dataclass, field

from .kinds import NodeKind


@dataclass(slots=True)
class Node:
    kind: NodeKind
    value: str | None = None
    children: list["Node"] = field(default_factory=list)

    def add(self, child: "Node") -> None:
        self.children.append(child)
