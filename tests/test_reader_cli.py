from __future__ import annotations

from pathlib import Path

import pytest

from pnfl_gameplanreader.reader_cli import main, parse_args

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
EXPECTED_DIR = TEST_DATA_DIR / "expected"
OFFENSE_PATH = TEST_DATA_DIR / "offense.pln"
DEFENSE_PATH = TEST_DATA_DIR / "defense.pln"


def _expected(name: str) -> list[str]:
    return (EXPECTED_DIR / name).read_text(encoding="utf-8").splitlines()


def _captured_stdout_lines(capsys: pytest.CaptureFixture[str]) -> list[str]:
    return capsys.readouterr().out.splitlines()


def _file_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


# ---------- argparse contract ----------


def test_parse_args_requires_gameplan_path() -> None:
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_default_sort_is_slot() -> None:
    args = parse_args(["offense.pln"])
    assert args.gameplan_path == "offense.pln"
    assert args.normal_out is None
    assert args.special_out is None
    assert args.sort == "slot"


def test_parse_args_accepts_output_path() -> None:
    args = parse_args(["offense.pln", "--normal-out", "plays.txt"])
    assert args.normal_out == "plays.txt"


def test_parse_args_accepts_output_special_path() -> None:
    args = parse_args(["offense.pln", "--special-out", "spec.txt"])
    assert args.special_out == "spec.txt"


def test_parse_args_accepts_dash_for_normal_stdout() -> None:
    args = parse_args(["offense.pln", "--normal-out", "-"])
    assert args.normal_out == "-"


def test_parse_args_accepts_dash_for_special_stdout() -> None:
    args = parse_args(["offense.pln", "--special-out", "-"])
    assert args.special_out == "-"


def test_parse_args_accepts_dash_for_both_stdout() -> None:
    args = parse_args(["offense.pln", "--normal-out", "-", "--special-out", "-"])
    assert args.normal_out == "-"
    assert args.special_out == "-"


def test_parse_args_rejects_same_file_for_both_outputs() -> None:
    with pytest.raises(SystemExit):
        parse_args(["offense.pln", "--normal-out", "same.txt", "--special-out", "same.txt"])


def test_parse_args_allows_dash_alongside_file() -> None:
    args = parse_args(["offense.pln", "--normal-out", "-", "--special-out", "spec.txt"])
    assert args.normal_out == "-"
    assert args.special_out == "spec.txt"


def test_parse_args_accepts_sort_name() -> None:
    args = parse_args(["offense.pln", "--sort", "name"])
    assert args.sort == "name"


def test_parse_args_rejects_invalid_sort() -> None:
    with pytest.raises(SystemExit):
        parse_args(["offense.pln", "--sort", "bogus"])


# ---------- default mode: stdout with headers (both sections) ----------


def test_main_default_offense_stdout_with_headers_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH)])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("offense_stdout.txt")


def test_main_default_defense_stdout_with_headers_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(DEFENSE_PATH)])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("defense_stdout.txt")


def test_main_default_offense_sort_name_with_headers_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--sort", "name"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("offense_by_name_stdout.txt")


# ---------- dash mode: stdout without headers (single section) ----------


def test_main_normal_dash_offense_stdout_without_header_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--normal-out", "-"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("offense_normal_by_slot_txt.txt")


def test_main_normal_dash_defense_stdout_without_header_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(DEFENSE_PATH), "--normal-out", "-"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("defense_normal_by_slot_txt.txt")


def test_main_special_dash_offense_stdout_without_header_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--special-out", "-"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("offense_special_txt.txt")


def test_main_special_dash_defense_stdout_without_header_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(DEFENSE_PATH), "--special-out", "-"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("defense_special_txt.txt")


# ---------- dash mode: stdout without headers (both sections combined) ----------


def test_main_both_dashes_offense_stdout_without_headers_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(OFFENSE_PATH), "--normal-out", "-", "--special-out", "-"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("offense_stdout_dash.txt")


def test_main_both_dashes_defense_stdout_without_headers_matches_fixture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([str(DEFENSE_PATH), "--normal-out", "-", "--special-out", "-"])
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("defense_stdout_dash.txt")


# ---------- file mode: write to disk without headers ----------


def test_main_normal_to_file_offense_matches_fixture(tmp_path: Path) -> None:
    out_path = tmp_path / "plays.txt"
    rc = main([str(OFFENSE_PATH), "--normal-out", str(out_path)])
    assert rc == 0
    assert _file_lines(out_path) == _expected("offense_normal_by_slot_txt.txt")


def test_main_normal_to_file_defense_matches_fixture(tmp_path: Path) -> None:
    out_path = tmp_path / "plays.txt"
    rc = main([str(DEFENSE_PATH), "--normal-out", str(out_path)])
    assert rc == 0
    assert _file_lines(out_path) == _expected("defense_normal_by_slot_txt.txt")


def test_main_special_to_file_offense_matches_fixture(tmp_path: Path) -> None:
    out_path = tmp_path / "spec.txt"
    rc = main([str(OFFENSE_PATH), "--special-out", str(out_path)])
    assert rc == 0
    assert _file_lines(out_path) == _expected("offense_special_txt.txt")


def test_main_special_to_file_defense_matches_fixture(tmp_path: Path) -> None:
    out_path = tmp_path / "spec.txt"
    rc = main([str(DEFENSE_PATH), "--special-out", str(out_path)])
    assert rc == 0
    assert _file_lines(out_path) == _expected("defense_special_txt.txt")


def test_main_both_to_separate_files_offense_match_fixtures(tmp_path: Path) -> None:
    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--normal-out",
            str(n_path),
            "--special-out",
            str(s_path),
        ]
    )
    assert rc == 0
    assert _file_lines(n_path) == _expected("offense_normal_by_slot_txt.txt")
    assert _file_lines(s_path) == _expected("offense_special_txt.txt")


def test_main_both_to_separate_files_defense_match_fixtures(tmp_path: Path) -> None:
    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    rc = main(
        [
            str(DEFENSE_PATH),
            "--normal-out",
            str(n_path),
            "--special-out",
            str(s_path),
        ]
    )
    assert rc == 0
    assert _file_lines(n_path) == _expected("defense_normal_by_slot_txt.txt")
    assert _file_lines(s_path) == _expected("defense_special_txt.txt")


def test_main_file_output_suppresses_stdout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out_path = tmp_path / "plays.txt"
    rc = main([str(OFFENSE_PATH), "--normal-out", str(out_path)])
    assert rc == 0
    assert capsys.readouterr().out == ""


def test_main_special_file_output_suppresses_stdout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out_path = tmp_path / "spec.txt"
    rc = main([str(OFFENSE_PATH), "--special-out", str(out_path)])
    assert rc == 0
    assert capsys.readouterr().out == ""


# ---------- mixed dash + file ----------


def test_main_normal_to_file_special_to_stdout_matches_fixtures(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    n_path = tmp_path / "n.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--normal-out",
            str(n_path),
            "--special-out",
            "-",
        ]
    )
    assert rc == 0
    assert _file_lines(n_path) == _expected("offense_normal_by_slot_txt.txt")
    assert _captured_stdout_lines(capsys) == _expected("offense_special_txt.txt")


def test_main_normal_to_stdout_special_to_file_matches_fixtures(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    s_path = tmp_path / "s.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--normal-out",
            "-",
            "--special-out",
            str(s_path),
        ]
    )
    assert rc == 0
    assert _captured_stdout_lines(capsys) == _expected("offense_normal_by_slot_txt.txt")
    assert _file_lines(s_path) == _expected("offense_special_txt.txt")


# ---------- sort behavior ----------


def test_main_sort_name_only_affects_normal_section(tmp_path: Path) -> None:
    n_path = tmp_path / "n.txt"
    s_path = tmp_path / "s.txt"
    rc = main(
        [
            str(OFFENSE_PATH),
            "--sort",
            "name",
            "--normal-out",
            str(n_path),
            "--special-out",
            str(s_path),
        ]
    )
    assert rc == 0
    assert _file_lines(n_path) == _expected("offense_normal_by_name_txt.txt")
    assert _file_lines(s_path) == _expected("offense_special_txt.txt")
