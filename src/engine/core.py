from pathlib import Path
import shutil


def run(input_path, output_path, level):
    input_dir = Path(input_path)
    output_dir = Path(output_path)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input path not found: {input_dir}")

    if output_dir.exists():
        shutil.rmtree(output_dir)

    shutil.copytree(input_dir, output_dir)

    return {
        "input": str(input_dir),
        "output": str(output_dir),
        "level": level,
        "status": "copied"
    }
