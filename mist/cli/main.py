from mist.core.context import Context
from mist.core.pipeline import Pipeline
from mist.passes.dummy import DummyPass


def main() -> None:
    context = Context()

    pipeline = Pipeline()
    pipeline.add(DummyPass())

    tree = object()

    pipeline.run(tree, context)

    for diagnostic in context.diagnostics.items:
        print(f"[{diagnostic.severity.name}] {diagnostic.message}")


if __name__ == "__main__":
    main()
