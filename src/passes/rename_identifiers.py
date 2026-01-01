import ast
import uuid
import builtins
import keyword


BUILTIN_NAMES = set(dir(builtins))
KEYWORDS = set(keyword.kwlist)


class IdentifierRenamer(ast.NodeTransformer):
    def __init__(self, rename_functions=True, rename_variables=True):
        self.mapping = {}
        self.rename_functions = rename_functions
        self.rename_variables = rename_variables

    def _should_rename(self, name):
        if name in BUILTIN_NAMES:
            return False
        if name in KEYWORDS:
            return False
        if name.startswith("__") and name.endswith("__"):
            return False
        return True

    def _new_name(self, original):
        if original not in self.mapping:
            self.mapping[original] = f"v_{uuid.uuid4().hex[:8]}"
        return self.mapping[original]

    def visit_FunctionDef(self, node):
        if self.rename_functions and self._should_rename(node.name):
            node.name = self._new_name(node.name)

        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        if self.rename_functions and self._should_rename(node.name):
            node.name = self._new_name(node.name)

        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        if self.rename_functions and self._should_rename(node.name):
            node.name = self._new_name(node.name)

        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if not self.rename_variables:
            return node

        if not self._should_rename(node.id):
            return node

        if isinstance(node.ctx, (ast.Store, ast.Load, ast.Param)):
            node.id = self._new_name(node.id)

        return node


def obfuscate_code(source_code, options=None):
    options = options or {}

    rename_functions = options.get("rename_functions", True)
    rename_variables = options.get("rename_variables", True)

    tree = ast.parse(source_code)

    transformer = IdentifierRenamer(
        rename_functions=rename_functions,
        rename_variables=rename_variables
    )

    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)

    return ast.unparse(tree)
