from mist.adapters.python.adapter import PythonAdapter


def main() -> None:

    source = """
name = "MIST"

print(f"Hello, {name}")
"""

    adapter = PythonAdapter()

    tree = adapter.parse(source)

    symbols = adapter.collect_symbols(tree)

    for symbol in symbols:
        print(
            symbol.id,
            symbol.kind.name,
            symbol.original_name,
        )


if __name__ == "__main__":
    main()
