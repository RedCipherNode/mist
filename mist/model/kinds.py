from __future__ import annotations

from enum import Enum, auto


class NodeKind(Enum):
    MODULE = auto()

    FUNCTION = auto()

    CLASS = auto()

    BLOCK = auto()

    PARAMETER = auto()

    IDENTIFIER = auto()

    ASSIGNMENT = auto()

    CALL = auto()

    RETURN = auto()

    IF = auto()

    WHILE = auto()

    FOR = auto()

    LITERAL = auto()

    EXPRESSION = auto()
