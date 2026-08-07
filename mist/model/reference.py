from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mist.model.symbol import Symbol


@dataclass(slots=True)
class Reference:
    symbol: Symbol

    node: Any

    is_definition: bool
