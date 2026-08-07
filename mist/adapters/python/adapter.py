from __future__ import annotations

import ast

from mist.model import Reference
from mist.model import Symbol
from mist.model import SymbolKind


# >>>>>----------------------------------------------<<<<<#
# Python Adapter
# >>>>>----------------------------------------------<<<<<#


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

        tree = RenameTransformer(symbols).visit(tree)
        tree = ConstantTransformer().visit(tree)

        ast.fix_missing_locations(tree)

        return tree

    def emit(self, tree: ast.AST) -> str:
        return ast.unparse(tree)


# >>>>>----------------------------------------------<<<<<#
# Symbol Collection
# >>>>>----------------------------------------------<<<<<#


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

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ):
        self._create(
            SymbolKind.FUNCTION,
            node.name,
            node,
        )
        self.generic_visit(node)

    def visit_withitem(
        self,
        node: ast.withitem,
    ):
        if isinstance(node.optional_vars, ast.Name):
            self._create(
                SymbolKind.VARIABLE,
                node.optional_vars.id,
                node.optional_vars,
            )
        self.generic_visit(node)

    def visit_For(
        self,
        node: ast.For,
    ):
        if isinstance(node.target, ast.Name):
            self._create(
                SymbolKind.VARIABLE,
                node.target.id,
                node.target,
            )
        self.generic_visit(node)

    def visit_comprehension(
        self,
        node: ast.comprehension,
    ):
        if isinstance(node.target, ast.Name):
            self._create(
                SymbolKind.VARIABLE,
                node.target.id,
                node.target,
            )
        self.generic_visit(node)

    def visit_alias(
        self,
        node: ast.alias,
    ):
        if node.asname is None:
            return

        self._create(
            SymbolKind.VARIABLE,
            node.asname,
            node,
        )


# >>>>>----------------------------------------------<<<<<#
# Reference Collection
# >>>>>----------------------------------------------<<<<<#


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


# >>>>>----------------------------------------------<<<<<#
# AST Rewrite
# >>>>>----------------------------------------------<<<<<#s


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

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ):

        new_name = self.map.get(node.name)

        if new_name is not None:
            node.name = new_name

        self.generic_visit(node)

        return node

    def visit_alias(
        self,
        node: ast.alias,
    ):

        if node.asname is None:
            return node

        new_name = self.map.get(node.asname)

        if new_name is not None:
            node.asname = new_name

        return node

    def visit_ExceptHandler(
        self,
        node: ast.ExceptHandler,
    ):
        if node.name is not None:
            new_name = self.map.get(node.name)

            if new_name is not None:
                node.name = new_name

        self.generic_visit(node)

        return node

    def visit_Global(
        self,
        node: ast.Global,
    ):
        node.names = [self.map.get(name, name) for name in node.names]

        return node

    def visit_Nonlocal(
        self,
        node: ast.Nonlocal,
    ):
        node.names = [self.map.get(name, name) for name in node.names]

        return node


# >>>>>----------------------------------------------<<<<<#
# Expression Generator
# >>>>>----------------------------------------------<<<<<#


import ast
import secrets


class ExpressionGenerator:
    def integer(
        self,
        value: int,
    ) -> ast.expr:

        strategies = [
            self._bitwise,
        ]

        strategy = secrets.choice(strategies)

        return strategy(value)

    def _bitwise(
        self,
        value: int,
    ) -> ast.expr:

        strategy = secrets.choice(
            [
                self._xor,
                self._shift,
                self._or,
            ]
        )

        return strategy(value)

    def _xor(
        self,
        value: int,
    ) -> ast.expr:

        if value <= 2:
            return ast.Constant(value=value)

        while True:
            left = secrets.randbits(16)

            if abs(left - value) < 32:
                continue

            right = left ^ value

            if right <= 2:
                continue

            return ast.BinOp(
                left=ast.Constant(left),
                op=ast.BitXor(),
                right=ast.Constant(right),
            )

    def _shift(
        self,
        value: int,
    ) -> ast.expr:

        if value <= 2:
            return ast.Constant(value=value)

        if value & 1:
            return ast.Constant(value=value)

        shift = 1

        return ast.BinOp(
            left=ast.Constant(value >> shift),
            op=ast.LShift(),
            right=ast.Constant(shift),
        )

    def _or(
        self,
        value: int,
    ) -> ast.expr:

        if value <= 2:
            return ast.Constant(value=value)

        while True:
            left = 0
            right = 0

            bit = 1
            temp = value

            while temp:
                if temp & 1:
                    if secrets.randbits(1):
                        left |= bit
                    else:
                        right |= bit

                bit <<= 1
                temp >>= 1

            if left == 0 or right == 0:
                continue

            return ast.BinOp(
                left=ast.Constant(left),
                op=ast.BitOr(),
                right=ast.Constant(right),
            )


class ConstantTransformer(ast.NodeTransformer):
    def __init__(self):
        self.generator = ExpressionGenerator()

    def visit_Constant(
        self,
        node: ast.Constant,
    ):

        if not isinstance(node.value, int):
            return node

        return self.generator.integer(node.value)
