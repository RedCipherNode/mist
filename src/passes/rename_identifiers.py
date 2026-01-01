import ast
import uuid


class IdentifierRenamer(ast.NodeTransformer):
    def __init__(self):
        self.mapping = {}

    def _new_name(self, original):
        if original not in self.mapping:
            self.mapping[original] = f"v_{uuid.uuid4().hex[:8]}"
        return self.mapping[original]

    def visit_FunctionDef(self, node):
        node.name = self._new_name(node.name)
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Load):
            node.id = self._new_name(node.id)
        return node


def obfuscate_code(source_code):
    tree = ast.parse(source_code)
    transformer = IdentifierRenamer()
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)
