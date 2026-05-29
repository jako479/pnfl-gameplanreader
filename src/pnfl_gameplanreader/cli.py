from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from pnfl_gameplanreader.gameplan_reader import GamePlanReader

PROG = "pnfl read-gameplan"
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
        prog=PROG,
        description="Read a .pln file and list plays from the gameplan.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Output routing:\n"
            "  --normal-out FILE   Write 64 normal plays to FILE (no header).\n"
            "  --special-out FILE  Write 10 custom special teams plays to FILE (no header).\n"
            "  Use '-' as FILE to send that section to stdout with no header.\n"
            "  When neither flag is given, both sections are printed to stdout with\n"
            "    '=== Normal ===' and '=== Special ===' headers for human reading.\n"
            "    This format is not consumable by pnfl write-gameplan; use the '-'\n"
            "    flags above when piping to the writer.\n"
            "  When both flags specify a file path, the paths must differ.\n"
            "\n"
            "Pipeline-friendly examples:\n"
            "  pnfl read-gameplan src.pln --normal-out - | pnfl write-gameplan dest.pln --normal-plays -\n"
            "  pnfl read-gameplan src.pln --normal-out - --special-out - | pnfl write-gameplan dest.pln --normal-plays - --special-plays -\n"  # noqa: E501
        ),
    )
    parser.add_argument("gameplan_path", help="Path to the .pln file")
    parser.add_argument(
        "--normal-out",
        dest="normal_out",
        metavar="FILE",
        help="Write the 64 normal plays to FILE (or '-' for stdout)",
    )
    parser.add_argument(
        "--special-out",
        dest="special_out",
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
    _validate_outputs(parser, args.normal_out, args.special_out)
    return args


def _validate_outputs(
    parser: argparse.ArgumentParser,
    normal_out: str | None,
    special_out: str | None,
) -> None:
    if normal_out is None or special_out is None:
        return
    if normal_out == STDOUT_TOKEN or special_out == STDOUT_TOKEN:
        return
    if Path(normal_out).resolve() == Path(special_out).resolve():
        parser.error("--normal-out and --special-out must point to different files")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    try:
        reader = GamePlanReader(args.gameplan_path)

        if args.normal_out is None and args.special_out is None:
            sys.stdout.write(f"{NORMAL_HEADER}\n")
            reader.write_normal_plays(sys.stdout, sort=args.sort)
            sys.stdout.write(f"\n{SPECIAL_HEADER}\n")
            reader.write_custom_special_plays(sys.stdout)
            return 0
        if args.normal_out is not None:
            with open_output(args.normal_out) as f:
                reader.write_normal_plays(f, sort=args.sort)
        if args.special_out is not None:
            with open_output(args.special_out) as f:
                reader.write_custom_special_plays(f)
    except OSError as error:
        print(f"{PROG}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
