"""`pnfl check-gameplan` — validate one or more `.pln` files against PNFL rules.

Accepts files and/or directories. Directories are scanned for `*.pln` at the
top level, or across the full tree with `-r/--recursive`. Each file is printed
with its violation count and a brief play-count summary; the run exits with
status 0 (clean), 1 (violations found), or 2 (usage / I/O error).
"""

from __future__ import annotations

import argparse
import glob
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

from pnfl_gameplan import (
    PNFL_RULES,
    InvalidGamePlanError,
    PnflGamePlan,
    Violation,
)
from pnfl_playpool import PlayPool, read_play_pool

from pnfl_gameplanreader.config import load_config

PROG = "pnfl check-gameplan"
_GLOB_CHARS = frozenset("*?[")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Validate one or more .pln gameplan files against the PNFL rule set.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Each PATH may be a .pln file or a directory.\n"
            "  Directory: every *.pln in the top level is checked.\n"
            "  Directory + -r: every *.pln in the tree is checked.\n"
            "\n"
            "Exit code: 0 = all clean, 1 = violations found, 2 = usage/I/O error.\n"
        ),
    )
    parser.add_argument(
        "paths",
        nargs="+",
        metavar="PATH",
        help="One or more .pln file or directory paths to check",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recurse into subdirectories when a PATH is a directory",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Use this INI file instead of the default config lookup",
    )
    parser.add_argument(
        "--play-path",
        dest="play_path",
        help="Path to PNFL play files directory (overrides config [Settings] PlayPath)",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(argv)


def collect_files(paths: Iterable[str], *, recursive: bool) -> tuple[list[Path], list[str]]:
    """Resolve each user-supplied path to a list of .pln files.

    Returns `(files, errors)`. Errors are one human-readable string per path
    that could not be resolved (missing, not a .pln, etc.). Each path may be:
    a file, a directory, or a glob pattern (containing `*`, `?`, or `[`).
    `cmd.exe` does not expand globs the way Unix shells do, so we expand them
    here ourselves — matching the implicit expansion that built-in commands
    like `dir` and `del` do. Glob matches are filtered to `.pln` files.
    Duplicate paths across inputs are de-duplicated while preserving first-seen
    order.
    """
    files: list[Path] = []
    seen: set[Path] = set()
    errors: list[str] = []
    for raw in paths:
        if _is_glob(raw):
            raw_matches = sorted(glob.glob(raw, recursive=True))
            matches = [Path(m) for m in raw_matches if Path(m).is_file() and Path(m).suffix.lower() == ".pln"]
            if not matches:
                errors.append(f"{raw}: no .pln files match")
                continue
            for match in matches:
                _add(match, files, seen)
            continue
        path = Path(raw)
        if not path.exists():
            errors.append(f"{raw}: path does not exist")
            continue
        if path.is_file():
            if path.suffix.lower() != ".pln":
                errors.append(f"{raw}: not a .pln file")
                continue
            _add(path, files, seen)
            continue
        # Directory.
        pattern = "**/*.pln" if recursive else "*.pln"
        dir_matches = sorted(path.glob(pattern))
        if not dir_matches:
            scope = "tree" if recursive else "directory"
            errors.append(f"{raw}: no .pln files in {scope}")
            continue
        for match in dir_matches:
            _add(match, files, seen)
    return files, errors


def _is_glob(s: str) -> bool:
    return any(c in s for c in _GLOB_CHARS)


def _add(path: Path, files: list[Path], seen: set[Path]) -> None:
    resolved = path.resolve()
    if resolved in seen:
        return
    seen.add(resolved)
    files.append(path)


def _format_summary_counts(pg: PnflGamePlan) -> str:
    normal = sum(1 for p in pg.normal_plays if p is not None)
    custom_special = sum(1 for p in pg.custom_special_plays if p is not None)
    return f"{normal} normal, {custom_special} custom special"


def _format_violation(v: Violation) -> str:
    prefix = f"[{v.pool_category}] " if v.pool_category else ""
    return f"{prefix}{v.message}"


def check_file(path: Path, play_pool: PlayPool) -> tuple[int, str]:
    """Validate one file and return (violation_count, line_for_stdout).

    On a parse error, returns (-1, error line). The summary loop treats -1 as
    a failure to check (not a violation count) and surfaces it in the I/O-error
    tally so the run exits 2.
    """
    try:
        pg = PnflGamePlan.from_file(str(path), PNFL_RULES, play_pool)
    except (OSError, InvalidGamePlanError) as error:
        return -1, f"{path}: ERROR: {error}"
    violations = pg.validate()
    counts = _format_summary_counts(pg)
    if not violations:
        return 0, f"{path}: OK ({counts})"
    lines = [f"{path}: {len(violations)} violation(s) ({counts})"]
    lines.extend(f"  {_format_violation(v)}" for v in violations)
    return len(violations), "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    files, path_errors = collect_files(args.paths, recursive=args.recursive)
    for error in path_errors:
        print(f"{PROG}: {error}", file=sys.stderr)
    if not files:
        return 2

    try:
        config = load_config(path=args.config, play_path=args.play_path)
        play_pool = read_play_pool(config.play_path)
    except (OSError, ValueError) as error:
        print(f"{PROG}: {error}", file=sys.stderr)
        return 2

    total_files = 0
    files_with_violations = 0
    total_violations = 0
    io_errors = 0
    for path in files:
        count, line = check_file(path, play_pool)
        print(line)
        total_files += 1
        if count < 0:
            io_errors += 1
        elif count > 0:
            files_with_violations += 1
            total_violations += count

    print()
    print(f"{total_files} file(s) checked, {total_violations} violation(s) across {files_with_violations} file(s).")
    if io_errors > 0 or path_errors:
        return 2
    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
