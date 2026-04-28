from __future__ import annotations

from pathlib import Path

import pytest

from fbpro98_gameplanreader.cli import main, parse_args


TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
OFFENSE_PATH = TEST_DATA_DIR / "offense.pln"


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


def test_main_writes_output_to_file(tmp_path: Path) -> None:
    if not OFFENSE_PATH.is_file():
        pytest.skip(f"Missing fixture: {OFFENSE_PATH}")
    output_path = tmp_path / "plays.txt"
    rc = main([str(OFFENSE_PATH), "--output", str(output_path)])
    assert rc == 0
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 64
    assert "OR45RL01" in lines


def test_main_prints_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    if not OFFENSE_PATH.is_file():
        pytest.skip(f"Missing fixture: {OFFENSE_PATH}")
    rc = main([str(OFFENSE_PATH)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "OR45RL01" in out
