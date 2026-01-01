import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR / "src"))

from engine.core import run


def parse_args():
    parser = argparse.ArgumentParser(
        description="Universal Obfuscation Tool"
    )

    parser.add_argument(
        "input",
        help="Input source folder to obfuscate"
    )

    parser.add_argument(
        "--output",
        default="dist",
        help="Output folder (default: dist)"
    )

    parser.add_argument(
        "--level",
        choices=["low", "medium", "high"],
        default="medium",
        help="Obfuscation level"
    )

    parser.add_argument(
        "--config",
        help="Path to config file"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    try:
        result = run(
            input_path=args.input,
            output_path=args.output,
            level=args.level
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("Universal Obfuscation Tool")
    print(f"Input  : {result['input']}")
    print(f"Output : {result['output']}")
    print(f"Level  : {result['level']}")
    print("Status : pipeline executed")



if __name__ == "__main__":
    main()
