from __future__ import annotations

import ast
from pathlib import Path

from mist.adapters.adapter import Adapter


class PythonAdapter(Adapter):
    @property
    def language(self) -> str:
        return "python"

    def supports(self, path: Path) -> bool:
        return path.suffix == ".py"

    def parse(self, source: str):
        return ast.parse(source)

    def emit(self, tree) -> str:
        return ast.unparse(tree)
