import ast


KEY = 23


class StringObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.used = False

    def _encode(self, value):
        return [ord(c) ^ KEY for c in value]

    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value:
            self.used = True
            encoded = self._encode(node.value)
            return ast.Call(
                func=ast.Name(id="_d", ctx=ast.Load()),
                args=[ast.List(elts=[ast.Constant(v) for v in encoded], ctx=ast.Load())],
                keywords=[]
            )
        return node


def obfuscate_strings(source_code):
    tree = ast.parse(source_code)
    transformer = StringObfuscator()
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)

    if not transformer.used:
        return ast.unparse(tree)

    decoder_stub = (
        "KEY = 23\n"
        "def _d(data):\n"
        "    return ''.join(chr(b ^ KEY) for b in data)\n\n"
    )

    return decoder_stub + ast.unparse(tree)
