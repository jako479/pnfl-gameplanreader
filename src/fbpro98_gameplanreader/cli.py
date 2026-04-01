from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from .gameplan_reader import GamePlanReader


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fbpro98-gameplanreader",
        description="Read a .pln file and list plays from the gameplan.",
    )
    parser.add_argument("gameplan", help="Path to the .pln file")
    parser.add_argument(
        "--output",
        help="Optional path to write the extracted play list",
    )
    parser.add_argument(
        "--sort",
        choices=("slot", "name"),
        default="slot",
        help="Sort output by slot order or alphabetically by name",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(argv)


def write_output(lines: list[str], output_path: str | None) -> None:
    output = "\n".join(lines)
    if output_path:
        Path(output_path).write_text(f"{output}\n", encoding="utf-8")
        return
    print(output)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    reader = GamePlanReader(args.gameplan)
    lines = reader.get_normal_plays(args.sort)
    write_output(lines, args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
