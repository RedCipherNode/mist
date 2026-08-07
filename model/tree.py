from __future__ import annotations

from dataclasses import dataclass

from .node import Node


@dataclass(slots=True)
class Tree:
    root: Node
