import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Universal Obfuscation Tool - Ready to use obfuscator"
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

    return parser.parse_args()


def main():
    args = parse_args()

    print("Universal Obfuscation Tool")
    print(f"Input  : {args.input}")
    print(f"Output : {args.output}")
    print(f"Level  : {args.level}")

    print("Obfuscation engine not implemented yet")
    print("CLI skeleton is working")


if __name__ == "__main__":
    main()
