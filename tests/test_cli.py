from __future__ import annotations

from pathlib import Path

import pytest

from fbpro98_gameplanreader.cli import main, parse_args

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
OFFENSE_PATH = TEST_DATA_DIR / "offense.pln"
DEFENSE_PATH = TEST_DATA_DIR / "defense.pln"

KNOWN_NORMAL_NAME = "OR45RL01"
KNOWN_SPECIAL_NAME = "BCFGPAT"


# ---------- argparse ----------


def test_parse_args_requires_gameplan() -> None:
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_defaults() -> None:
    args = parse_args(["offense.pln"])
    assert args.gameplan_path == "offense.pln"
    assert args.output is None
    assert args.output_special is None
    assert args.sort == "slot"


def test_parse_args_accepts_output_only() -> None:
    args = parse_args(["offense.pln", "--output", "plays.txt"])
    assert args.output == "plays.txt"
    assert args.output_special is None


def test_parse_args_accepts_output_special_only() -> None:
    args = parse_args(["offense.pln", "--output-special", "spec.txt"])
    assert args.output is None
    assert args.output_special == "spec.txt"


def test_parse_args_accepts_both_output_flags() -> None:
    args = parse_args(["offense.pln", "--output", "n.txt", "--output-special", "s.txt"])
    assert args.output == "n.txt"
    assert args.output_special == "s.txt"


def test_parse_args_accepts_dash_for_normal() -> None:
    args = parse_args(["offense.pln", "--output", "-"])
    assert args.output == "-"


def test_parse_args_accepts_dash_for_special() -> None:
    args = parse_args(["offense.pln", "--output-special", "-"])
    assert args.output_special == "-"


def test_parse_args_accepts_dash_for_both() -> None:
    args = parse_args(["offense.pln", "--output", "-", "--output-special", "-"])
    assert args.output == "-"
    assert args.output_special == "-"


def test_parse_args_rejects_same_file_for_both() -> None:
    with pytest.raises(SystemExit):
        parse_args(["offense.pln", "--output", "same.txt", "--output-special", "same.txt"])


def test_parse_args_allows_dash_alongside_file() -> None:
    args = parse_args(["offense.pln", "--output", "-", "--output-special", "spec.txt"])
    assert args.output == "-"
    assert args.output_special == "spec.txt"


def test_parse_args_accepts_sort_name() -> None:
    args = parse_args(["offense.pln", "--sort", "name"])
    assert args.sort == "name"


def test_parse_args_rejects_invalid_sort() -> None:
    with pytest.raises(SystemExit):
        parse_args(["offense.pln", "--sort", "bogus"])


# ---------- main: default (no flags) prints both with headers ----------


def test_main_default_prints_both_sections_with_headers(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "=== Normal ===" in out
    assert "=== Special ===" in out
    # Normal precedes Special
    assert out.index("=== Normal ===") < out.index("=== Special ===")
    assert KNOWN_NORMAL_NAME in out
    assert KNOWN_SPECIAL_NAME in out


def test_main_default_special_header_follows_normal_section(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH)])
    assert rc == 0
    out = capsys.readouterr().out
    # The special header follows the last normal play directly.
    assert "\n=== Special ===" in out


# ---------- main: --output FILE only ----------


def test_main_normal_only_to_file_no_header(tmp_path: Path) -> None:
    output_path = tmp_path / "plays.txt"
    rc = main([str(OFFENSE_PATH), "--output", str(output_path)])
    assert rc == 0
    text = output_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert len(lines) == 64
    assert "===" not in text
    assert KNOWN_NORMAL_NAME in lines
    assert KNOWN_SPECIAL_NAME not in lines


def test_main_normal_only_to_file_does_not_emit_to_stdout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output_path = tmp_path / "plays.txt"
    rc = main([str(OFFENSE_PATH), "--output", str(output_path)])
    assert rc == 0
    out = capsys.readouterr().out
    assert out == ""


# ---------- main: --output-special FILE only ----------


def test_main_special_only_to_file_no_header_with_blanks(tmp_path: Path) -> None:
    output_path = tmp_path / "spec.txt"
    rc = main([str(OFFENSE_PATH), "--output-special", str(output_path)])
    assert rc == 0
    text = output_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert len(lines) == 10
    assert "===" not in text
    assert lines[0] == "BCFGPAT"
    # Slots 5-8 are empty in offense fixture
    assert lines[4] == ""
    assert lines[5] == ""
    assert lines[6] == ""
    assert lines[7] == ""
    assert KNOWN_NORMAL_NAME not in lines


# ---------- main: both --output and --output-special as files ----------


def test_main_both_to_files_writes_each_section(tmp_path: Path) -> None:
    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--output",
            str(n_path),
            "--output-special",
            str(s_path),
        ]
    )
    assert rc == 0
    n_lines = n_path.read_text(encoding="utf-8").splitlines()
    s_lines = s_path.read_text(encoding="utf-8").splitlines()
    assert len(n_lines) == 64
    assert len(s_lines) == 10
    assert KNOWN_NORMAL_NAME in n_lines
    assert KNOWN_SPECIAL_NAME in s_lines


# ---------- main: dash variants ----------


def test_main_dash_for_normal_to_stdout_no_header(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--output", "-"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "===" not in out
    assert KNOWN_NORMAL_NAME in out
    assert KNOWN_SPECIAL_NAME not in out
    lines = out.splitlines()
    assert len(lines) == 64


def test_main_dash_for_special_to_stdout_no_header(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--output-special", "-"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "===" not in out
    assert KNOWN_SPECIAL_NAME in out
    assert KNOWN_NORMAL_NAME not in out
    lines = out.splitlines()
    assert len(lines) == 10


def test_main_dash_for_both_normal_first_no_separator(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--output", "-", "--output-special", "-"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "===" not in out
    lines = out.splitlines()
    assert len(lines) == 74  # 64 normal + 10 special, no separator
    # Normal first
    assert lines[0] == "OR45RL01"
    assert KNOWN_SPECIAL_NAME in lines[64:]


def test_main_mixed_dash_and_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    n_path = tmp_path / "n.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--output",
            str(n_path),
            "--output-special",
            "-",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "===" not in out
    assert KNOWN_SPECIAL_NAME in out
    assert KNOWN_NORMAL_NAME not in out
    n_lines = n_path.read_text(encoding="utf-8").splitlines()
    assert len(n_lines) == 64
    assert KNOWN_NORMAL_NAME in n_lines


# ---------- sort behavior ----------


def test_main_sort_name_only_affects_normal(tmp_path: Path) -> None:
    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--sort",
            "name",
            "--output",
            str(n_path),
            "--output-special",
            str(s_path),
        ]
    )
    assert rc == 0
    n_lines = n_path.read_text(encoding="utf-8").splitlines()
    # name-sorted normal: AF1AwagR is first in the EXPECTED_OFFENSE_BY_NAME list
    assert n_lines[0] == "AF1AwagR"
    s_lines = s_path.read_text(encoding="utf-8").splitlines()
    # special is always slot order; first slot is BCFGPAT in offense fixture
    assert s_lines[0] == "BCFGPAT"


# ---------- defense gameplan basics ----------


def test_main_default_works_on_defense(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(DEFENSE_PATH)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "=== Normal ===" in out
    assert "=== Special ===" in out
    assert "NY31RL01" in out  # known normal in defense fixture
    assert "CIN-KR" in out  # known special in defense fixture


def test_main_special_only_for_defense_to_file_with_leading_blank(
    tmp_path: Path,
) -> None:
    s_path = tmp_path / "s.txt"
    rc = main([str(DEFENSE_PATH), "--output-special", str(s_path)])
    assert rc == 0
    lines = s_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 10
    # Defense fixture has empty slot at index 0 (no FG/PAT defense set)
    assert lines[0] == ""
    assert lines[1] == "CIN-KR"
