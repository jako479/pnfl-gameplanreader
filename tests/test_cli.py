from __future__ import annotations

import pytest

from fbpro98_gameplanreader.cli import parse_args


def test_parse_args_requires_gameplan() -> None:
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_accepts_gameplan() -> None:
    args = parse_args(["offense.pln"])
    assert args.gameplan == "offense.pln"
    assert args.output is None
    assert args.sort == "slot"


def test_parse_args_accepts_output() -> None:
    args = parse_args(["offense.pln", "--output", "plays.txt"])
    assert args.output == "plays.txt"


def test_parse_args_accepts_sort_name() -> None:
    args = parse_args(["offense.pln", "--sort", "name"])
    assert args.sort == "name"


def test_parse_args_rejects_invalid_sort() -> None:
    with pytest.raises(SystemExit):
        parse_args(["offense.pln", "--sort", "bogus"])
