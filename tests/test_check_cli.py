from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from pnfl_gameplan import PnflGamePlan

from pnfl_gameplanreader.check_cli import check_file, collect_files, main, parse_args

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
OFFENSE_PATH = TEST_DATA_DIR / "offense.pln"
DEFENSE_PATH = TEST_DATA_DIR / "defense.pln"
PLAYPOOL_DIR = Path(__file__).resolve().parents[2] / "pnfl-playpool" / "tests" / "data" / "plays"


# ---------- argparse ----------


def test_parse_args_requires_at_least_one_path() -> None:
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_defaults() -> None:
    args = parse_args(["a.pln"])
    assert args.paths == ["a.pln"]
    assert args.recursive is False
    assert args.config is None
    assert args.play_path is None


def test_parse_args_recursive_flag() -> None:
    args = parse_args(["dir", "-r"])
    assert args.recursive is True


# ---------- file collection ----------


def test_collect_files_single_file(tmp_path: Path) -> None:
    f = tmp_path / "a.pln"
    f.touch()
    files, errors = collect_files([str(f)], recursive=False)
    assert files == [f]
    assert errors == []


def test_collect_files_directory_top_level_only(tmp_path: Path) -> None:
    (tmp_path / "a.pln").touch()
    (tmp_path / "b.pln").touch()
    (tmp_path / "skip.txt").touch()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "deep.pln").touch()

    files, errors = collect_files([str(tmp_path)], recursive=False)
    names = sorted(f.name for f in files)
    assert names == ["a.pln", "b.pln"]
    assert errors == []


def test_collect_files_directory_recursive(tmp_path: Path) -> None:
    (tmp_path / "top.pln").touch()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "deep.pln").touch()
    (tmp_path / "sub" / "sub2").mkdir()
    (tmp_path / "sub" / "sub2" / "deeper.pln").touch()

    files, errors = collect_files([str(tmp_path)], recursive=True)
    names = sorted(f.name for f in files)
    assert names == ["deep.pln", "deeper.pln", "top.pln"]
    assert errors == []


def test_collect_files_missing_path_reports_error(tmp_path: Path) -> None:
    nope = tmp_path / "nope"
    files, errors = collect_files([str(nope)], recursive=False)
    assert files == []
    assert any("does not exist" in e for e in errors)


def test_collect_files_non_pln_file_reports_error(tmp_path: Path) -> None:
    bad = tmp_path / "not_pln.txt"
    bad.touch()
    files, errors = collect_files([str(bad)], recursive=False)
    assert files == []
    assert any("not a .pln file" in e for e in errors)


def test_collect_files_empty_directory_reports_error(tmp_path: Path) -> None:
    files, errors = collect_files([str(tmp_path)], recursive=False)
    assert files == []
    assert any("no .pln files" in e for e in errors)


def test_collect_files_dedupes_repeats(tmp_path: Path) -> None:
    f = tmp_path / "a.pln"
    f.touch()
    files, _ = collect_files([str(f), str(f)], recursive=False)
    assert len(files) == 1


def test_collect_files_expands_glob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "Off1.pln").touch()
    (tmp_path / "Off2.pln").touch()
    (tmp_path / "Def.pln").touch()
    (tmp_path / "skip.txt").touch()
    monkeypatch.chdir(tmp_path)

    files, errors = collect_files(["Off*.pln"], recursive=False)
    names = sorted(f.name for f in files)
    assert names == ["Off1.pln", "Off2.pln"]
    assert errors == []


def test_collect_files_recursive_glob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "top.pln").touch()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "deep.pln").touch()
    monkeypatch.chdir(tmp_path)

    files, errors = collect_files(["**/*.pln"], recursive=False)
    names = sorted(f.name for f in files)
    assert names == ["deep.pln", "top.pln"]
    assert errors == []


def test_collect_files_glob_matches_nothing_reports_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "x.txt").touch()
    monkeypatch.chdir(tmp_path)

    files, errors = collect_files(["*.pln"], recursive=False)
    assert files == []
    assert any("no .pln files match" in e for e in errors)


def test_collect_files_glob_filters_to_pln(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "a.pln").touch()
    (tmp_path / "b.txt").touch()
    monkeypatch.chdir(tmp_path)

    files, errors = collect_files(["*"], recursive=False)
    assert [f.name for f in files] == ["a.pln"]
    assert errors == []


# ---------- check_file ----------


def test_check_file_violations_format(tmp_path: Path) -> None:
    pln = tmp_path / "offense.pln"
    shutil.copy2(OFFENSE_PATH, pln)
    from pnfl_playpool import read_play_pool

    pool = read_play_pool(str(PLAYPOOL_DIR))
    count, line = check_file(pln, pool)
    assert count > 0
    head, *rest = line.splitlines()
    assert head.startswith(str(pln))
    assert "violation(s)" in head
    assert "60 normal, 6 custom special" in head
    # Per-violation lines indent with two spaces and (where present) are prefixed
    # with the pool category in brackets.
    assert all(detail.startswith("  ") for detail in rest)


def test_check_file_clean_format(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    pln = tmp_path / "offense.pln"
    shutil.copy2(OFFENSE_PATH, pln)
    from pnfl_playpool import read_play_pool

    pool = read_play_pool(str(PLAYPOOL_DIR))
    monkeypatch.setattr(PnflGamePlan, "validate", lambda self: ())

    count, line = check_file(pln, pool)
    assert count == 0
    assert line == f"{pln}: OK (60 normal, 6 custom special)"


def test_check_file_malformed_pln_returns_error(tmp_path: Path) -> None:
    """Malformed .pln triggers the InvalidGamePlanError path: (-1, ERROR line)."""
    bad = tmp_path / "broken.pln"
    bad.write_bytes(b"\x00\x01\x02")  # too small for the G95 header
    from pnfl_playpool import read_play_pool

    pool = read_play_pool(str(PLAYPOOL_DIR))
    count, line = check_file(bad, pool)
    assert count == -1
    assert line.startswith(f"{bad}: ERROR")


# ---------- main ----------


def test_main_violations_exit_1(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main([str(OFFENSE_PATH), "--play-path", str(PLAYPOOL_DIR)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "violation(s)" in out
    assert "1 file(s) checked" in out


def test_main_multiple_files_summary(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main([str(OFFENSE_PATH), str(DEFENSE_PATH), "--play-path", str(PLAYPOOL_DIR)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "2 file(s) checked" in out
    assert "across 2 file(s)" in out


def test_main_missing_path_exit_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc = main([str(tmp_path / "nope.pln")])
    assert rc == 2
    err = capsys.readouterr().err
    assert "does not exist" in err


def test_main_malformed_pln_exit_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """File exists but parse fails → check_file returns -1, io_errors bumps → exit 2."""
    bad = tmp_path / "broken.pln"
    bad.write_bytes(b"\x00\x01\x02")
    rc = main([str(bad), "--play-path", str(PLAYPOOL_DIR)])
    assert rc == 2
    out = capsys.readouterr().out
    assert "ERROR" in out


def test_main_directory_scans_pln_files(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    shutil.copy2(OFFENSE_PATH, tmp_path / "off.pln")
    shutil.copy2(DEFENSE_PATH, tmp_path / "def.pln")

    rc = main([str(tmp_path), "--play-path", str(PLAYPOOL_DIR)])
    assert rc == 1  # both fixtures have known violations
    out = capsys.readouterr().out
    assert "2 file(s) checked" in out


def test_main_recursive_scans_subdirs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    sub = tmp_path / "sub"
    sub.mkdir()
    shutil.copy2(OFFENSE_PATH, sub / "off.pln")

    rc = main([str(tmp_path), "-r", "--play-path", str(PLAYPOOL_DIR)])
    assert rc == 1
    out = capsys.readouterr().out
    assert "1 file(s) checked" in out


def test_main_clean_exit_0(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    shutil.copy2(OFFENSE_PATH, tmp_path / "off.pln")
    monkeypatch.setattr(PnflGamePlan, "validate", lambda self: ())

    rc = main([str(tmp_path / "off.pln"), "--play-path", str(PLAYPOOL_DIR)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "OK" in out
    assert "0 violation(s) across 0 file(s)" in out
