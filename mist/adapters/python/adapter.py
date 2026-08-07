from __future__ import annotations

import ast

from mist.model import Reference
from mist.model import Symbol
from mist.model import SymbolKind


class PythonAdapter:
    def parse(self, source: str) -> ast.AST:
        return ast.parse(source)

    def collect_symbols(self, tree: ast.AST) -> list[Symbol]:

        collector = SymbolCollector()
        collector.visit(tree)

        references = ReferenceCollector(collector.index)
        references.visit(tree)

        return collector.symbols

    def rewrite(
        self,
        tree: ast.AST,
        symbols: list[Symbol],
    ) -> ast.AST:

        transformer = RenameTransformer(symbols)

        return transformer.visit(tree)

    def emit(self, tree: ast.AST) -> str:
        return ast.unparse(tree)


class SymbolCollector(ast.NodeVisitor):
    def __init__(self) -> None:

        self.symbols: list[Symbol] = []
        self.index: dict[str, Symbol] = {}

        self._next_id = 0

    def _create(
        self,
        kind: SymbolKind,
        name: str,
        node: ast.AST,
    ) -> Symbol:

        symbol = Symbol(
            id=self._next_id,
            kind=kind,
            original_name=name,
            node=node,
        )

        self._next_id += 1

        self.symbols.append(symbol)
        self.index[name] = symbol

        return symbol

    def visit_FunctionDef(self, node: ast.FunctionDef):

        self._create(
            SymbolKind.FUNCTION,
            node.name,
            node,
        )

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):

        self._create(
            SymbolKind.CLASS,
            node.name,
            node,
        )

        self.generic_visit(node)

    def visit_arg(self, node: ast.arg):

        self._create(
            SymbolKind.PARAMETER,
            node.arg,
            node,
        )

    def visit_Name(self, node: ast.Name):

        if isinstance(node.ctx, ast.Store):
            self._create(
                SymbolKind.VARIABLE,
                node.id,
                node,
            )

        self.generic_visit(node)


class ReferenceCollector(ast.NodeVisitor):
    def __init__(
        self,
        index: dict[str, Symbol],
    ) -> None:

        self.index = index

    def visit_Name(self, node: ast.Name):

        symbol = self.index.get(node.id)

        if symbol is not None:
            symbol.references.append(
                Reference(
                    symbol=symbol,
                    node=node,
                    is_definition=isinstance(
                        node.ctx,
                        ast.Store,
                    ),
                )
            )

        self.generic_visit(node)


class RenameTransformer(ast.NodeTransformer):
    def __init__(self, symbols: list[Symbol]) -> None:

        self.map = {
            symbol.original_name: symbol.obfuscated_name
            for symbol in symbols
            if symbol.obfuscated_name is not None
        }

    def visit_Name(self, node: ast.Name):

        new_name = self.map.get(node.id)

        if new_name is not None:
            node.id = new_name

        return self.generic_visit(node)

    def visit_arg(self, node: ast.arg):

        new_name = self.map.get(node.arg)

        if new_name is not None:
            node.arg = new_name

        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):

        new_name = self.map.get(node.name)

        if new_name is not None:
            node.name = new_name

        self.generic_visit(node)

        return node

    def visit_ClassDef(self, node: ast.ClassDef):

        new_name = self.map.get(node.name)

        if new_name is not None:
            node.name = new_name

        self.generic_visit(node)

        return node
