from mist.core.base_pass import BasePass


class DummyPass(BasePass):
    @property
    def name(self) -> str:
        return "dummy"

    def run(self, tree, context):
        context.diagnostics.info("Dummy pass executed.")
        return tree
