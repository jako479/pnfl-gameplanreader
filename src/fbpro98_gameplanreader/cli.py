from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from fbpro98_gameplanreader.gameplan_reader import GamePlanReader

STDOUT_TOKEN = "-"
NORMAL_HEADER = "=== Normal ==="
SPECIAL_HEADER = "=== Special ==="


@contextmanager
def open_output(dest: str) -> Iterator[TextIO]:
    """Yield a writable text stream for ``dest``.

    A dest of '-' yields ``sys.stdout`` and never closes it. Any other value
    is treated as a filesystem path opened for writing in UTF-8.
    """
    if dest == STDOUT_TOKEN:
        yield sys.stdout
        return
    with open(dest, "w", encoding="utf-8") as f:
        yield f


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pnfl read-gameplan",
        description="Read a .pln file and list plays from the gameplan.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Output routing:\n"
            "  --output FILE          Write 64 normal plays to FILE (no header).\n"
            "  --output-special FILE  Write 10 custom special teams plays to FILE (no header).\n"
            "  Use '-' as FILE to send that section to stdout with no header.\n"
            "  When neither flag is given, both sections are printed to stdout\n"
            "    with '=== Normal ===' and '=== Special ===' headers.\n"
            "  When both flags specify a file path, the paths must differ.\n"
            "\n"
            "Pipeline-friendly examples:\n"
            "  pnfl read-gameplan src.pln | pnfl write-gameplan dest.pln --normal-plays -\n"
            "  pnfl read-gameplan src.pln --output - --output-special - | ...\n"
        ),
    )
    parser.add_argument("gameplan_path", help="Path to the .pln file")
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write the 64 normal plays to FILE (or '-' for stdout)",
    )
    parser.add_argument(
        "--output-special",
        dest="output_special",
        metavar="FILE",
        help="Write the 10 custom special teams plays to FILE (or '-' for stdout)",
    )
    parser.add_argument(
        "--sort",
        choices=("slot", "name"),
        default="slot",
        help="Sort order for the normal plays (default: %(default)s)",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    _validate_outputs(parser, args.output, args.output_special)
    return args


def _validate_outputs(
    parser: argparse.ArgumentParser,
    output: str | None,
    output_special: str | None,
) -> None:
    if output is None or output_special is None:
        return
    if output == STDOUT_TOKEN or output_special == STDOUT_TOKEN:
        return
    if Path(output).resolve() == Path(output_special).resolve():
        parser.error("--output and --output-special must point to different files")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    reader = GamePlanReader(args.gameplan_path)

    if args.output is None and args.output_special is None:
        sys.stdout.write(f"{NORMAL_HEADER}\n")
        reader.write_normal_plays(sys.stdout, sort=args.sort)
        sys.stdout.write(f"{SPECIAL_HEADER}\n")
        reader.write_custom_special_plays(sys.stdout)
        return 0
    if args.output is not None:
        with open_output(args.output) as f:
            reader.write_normal_plays(f, sort=args.sort)
    if args.output_special is not None:
        with open_output(args.output_special) as f:
            reader.write_custom_special_plays(f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
