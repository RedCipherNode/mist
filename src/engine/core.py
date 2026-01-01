from passes.rename_identifiers import obfuscate_code
from pathlib import Path
import shutil

from passes.rename_identifiers import obfuscate_code


def run(input_path, output_path, config, level):
    input_dir = Path(input_path)
    output_dir = Path(output_path)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input path not found: {input_dir}")

    if output_dir.exists():
        shutil.rmtree(output_dir)

    shutil.copytree(input_dir, output_dir)

    for py_file in output_dir.rglob("*.py"):
        source = py_file.read_text(encoding="utf-8")
        obfuscated = obfuscate_code(source)
        py_file.write_text(obfuscated, encoding="utf-8")

    level = config.get("level", "medium")

    return {
        "input": str(input_dir),
        "output": str(output_dir),
        "level": level,
        "status": "obfuscated"
}

