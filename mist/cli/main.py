from pathlib import Path

from mist.adapters.python.adapter import PythonAdapter
from mist.passes.rename import RenamePass


def main() -> None:

    source = Path("hello.py").read_text(
        encoding="utf-8",
    )

    adapter = PythonAdapter()

    # Parse source
    tree = adapter.parse(source)

    # Collect symbols
    symbols = adapter.collect_symbols(tree)

    # Generate obfuscated names
    RenamePass().rename(symbols)

    # Rewrite AST
    tree = adapter.rewrite(
        tree,
        symbols,
    )

    # Emit source code
    output = adapter.emit(tree)

    # Debug
    print("=" * 35)
    print(output)
    print("=" * 35)

    # Write file
    Path("hello_obf.py").write_text(
        output,
        encoding="utf-8",
    )

    print("Generated: output.py")


if __name__ == "__main__":
    main()
