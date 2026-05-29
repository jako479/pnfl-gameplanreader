from __future__ import annotations

from io import StringIO
from pathlib import Path

from pnfl_gameplanreader.gameplan_reader import GamePlanReader

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
EXPECTED_DIR = TEST_DATA_DIR / "expected"
OFFENSE_PATH = TEST_DATA_DIR / "offense.pln"
DEFENSE_PATH = TEST_DATA_DIR / "defense.pln"


def _expected(name: str) -> list[str]:
    return (EXPECTED_DIR / name).read_text(encoding="utf-8").splitlines()


# ---------- get_normal_plays ----------


def test_get_normal_plays_offense_slot_order_matches_fixture() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_normal_plays("slot") == _expected("offense_normal_by_slot_txt.txt")


def test_get_normal_plays_offense_name_order_matches_fixture() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_normal_plays("name") == _expected("offense_normal_by_name_txt.txt")


def test_get_normal_plays_defense_slot_order_matches_fixture() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    assert reader.get_normal_plays("slot") == _expected("defense_normal_by_slot_txt.txt")


def test_get_normal_plays_defense_name_order_matches_fixture() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    assert reader.get_normal_plays("name") == _expected("defense_normal_by_name_txt.txt")


def test_get_normal_plays_default_sort_is_slot() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_normal_plays() == reader.get_normal_plays("slot")


def test_get_normal_plays_returns_exactly_64_in_slot_mode() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert len(reader.get_normal_plays("slot")) == 64


def test_get_normal_plays_filters_blanks_in_name_mode() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert "" not in reader.get_normal_plays("name")


# ---------- get_custom_special_plays ----------


def test_get_custom_special_plays_offense_matches_fixture() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_custom_special_plays() == _expected("offense_special_txt.txt")


def test_get_custom_special_plays_defense_matches_fixture() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    assert reader.get_custom_special_plays() == _expected("defense_special_txt.txt")


def test_get_custom_special_plays_returns_exactly_ten() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert len(reader.get_custom_special_plays()) == 10


def test_get_custom_special_plays_blank_for_empty_slot() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    plays = reader.get_custom_special_plays()
    # Slots 5-8 (indices 4-7) are empty in the offense fixture
    for i in range(4, 8):
        assert plays[i] == ""


# ---------- write_normal_plays / write_custom_special_plays ----------


def test_write_normal_plays_offense_slot_matches_fixture() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out)
    assert out.getvalue().splitlines() == _expected("offense_normal_by_slot_txt.txt")


def test_write_normal_plays_offense_name_matches_fixture() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out, sort="name")
    assert out.getvalue().splitlines() == _expected("offense_normal_by_name_txt.txt")


def test_write_normal_plays_emits_no_header() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out)
    assert "===" not in out.getvalue()


def test_write_custom_special_plays_offense_matches_fixture() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_custom_special_plays(out)
    assert out.getvalue().splitlines() == _expected("offense_special_txt.txt")


def test_write_custom_special_plays_defense_matches_fixture() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    out = StringIO()
    reader.write_custom_special_plays(out)
    assert out.getvalue().splitlines() == _expected("defense_special_txt.txt")


def test_write_custom_special_plays_emits_no_header() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_custom_special_plays(out)
    assert "===" not in out.getvalue()


def test_write_methods_round_trip_via_get_methods() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out)
    expected = "\n".join(reader.get_normal_plays()) + "\n"
    assert out.getvalue() == expected
