from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class SymbolKind(Enum):
    MODULE = auto()
    CLASS = auto()
    FUNCTION = auto()
    METHOD = auto()
    PARAMETER = auto()
    VARIABLE = auto()
    ATTRIBUTE = auto()
    IMPORT = auto()


@dataclass(slots=True)
class Symbol:
    id: int
    kind: SymbolKind

    original_name: str
    obfuscated_name: str | None = None

    node: Any | None = None
    scope: Any | None = None
