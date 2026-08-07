from mist.adapters.python.adapter import PythonAdapter


def main() -> None:
    adapter = PythonAdapter()

    source = """
name = "MIST"

print(f"Hello, {name}")
"""

    tree = adapter.parse(source)

    output = adapter.emit(tree)

    print(output)


if __name__ == "__main__":
    main()
