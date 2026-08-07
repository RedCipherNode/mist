from __future__ import annotations

import ast

from mist.model import Symbol
from mist.model import SymbolKind


class PythonAdapter:
    def parse(self, source: str) -> ast.AST:
        return ast.parse(source)

    def collect_symbols(self, tree: ast.AST) -> list[Symbol]:

        collector = SymbolCollector()
        collector.visit(tree)

        return collector.symbols

    def rewrite(self, tree, symbols):
        return tree

    def emit(self, tree) -> str:
        return ast.unparse(tree)


class SymbolCollector(ast.NodeVisitor):
    def __init__(self):

        self.symbols: list[Symbol] = []
        self._next_id = 0

    def _create(self, kind, name, node):

        symbol = Symbol(
            id=self._next_id,
            kind=kind,
            original_name=name,
            node=node,
        )

        self._next_id += 1

        self.symbols.append(symbol)

    def visit_arg(self, node):

        self._create(
            SymbolKind.PARAMETER,
            node.arg,
            node,
        )

    def visit_Name(self, node):

        if isinstance(node.ctx, ast.Store):
            self._create(
                SymbolKind.VARIABLE,
                node.id,
                node,
            )

        self.generic_visit(node)

    def visit_ClassDef(self, node):

        self._create(
            SymbolKind.CLASS,
            node.name,
            node,
        )

        self.generic_visit(node)

    def visit_ClassDef(self, node):

        self._create(
            SymbolKind.CLASS,
            node.name,
            node,
        )

        self.generic_visit(node)
