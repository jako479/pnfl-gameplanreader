from io import StringIO
from pathlib import Path

from fbpro98_gameplanreader.gameplan_reader import GamePlanReader

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
OFFENSE_PATH = TEST_DATA_DIR / "offense.pln"
DEFENSE_PATH = TEST_DATA_DIR / "defense.pln"

EXPECTED_OFFENSE_BY_SLOT = [
    "OR45RL01",
    "OR10RLRG",
    "SF35Hevy",
    "OR36RL01",
    "SF67Swp1",
    "DB57rrLT",
    "TT10draw",
    "NE28RRS1",
    "NY26RM00",
    "KC27swp3",
    "ORX8rmT2",
    "MN22tctr",
    "NY23rmV3",
    "ATF27swp",
    "SF28ore2",
    "SF22orc1",
    "SF25olt5",
    "JJ10drw3",
    "DC28RM01",
    "LVXglp01",
    "ATGZsloT",
    "ATFGsloT",
    "JJ1YBblT",
    "NE1YCrsX",
    "SF1YemTy",
    "AF1AwagR",
    "LA1Hfire",
    "SF1UemTy",
    "JJ2IBblT",
    "",
    "DC2YT01",
    "LV2JscrT",
    "KC2IFLYX",
    "KC2ArolR",
    "OR3ZshtZ",
    "NE3YbblT",
    "",
    "",
    "SF3YzipT",
    "JJ7XFloA",
    "AT7AwgRT",
    "JJ7HWagR",
    "OR4XRp90",
    "SF7XsTop",
    "SF4XmimA",
    "NY7HhoT",
    "JJ8HCnrT",
    "NY8Gpt3",
    "ATF5BTSz",
    "DBA5XgoY",
    "LAC8XSln",
    "JJ6ZWAGR",
    "SF6BspoT",
    "NE6H01",
    "MN6XLuckT",
    "",
    "SF9Zdout",
    "SF9ZflyA",
    "OR91FLYX",
    "DB9ZW2",
    "LA0ZSLOB",
    "SF0BlofT",
    "OR0HSnap",
    "SF0XrazZ",
]

EXPECTED_OFFENSE_BY_NAME = [
    "AF1AwagR",
    "AT7AwgRT",
    "ATF27swp",
    "ATF5BTSz",
    "ATFGsloT",
    "ATGZsloT",
    "DB57rrLT",
    "DB9ZW2",
    "DBA5XgoY",
    "DC28RM01",
    "DC2YT01",
    "JJ10drw3",
    "JJ1YBblT",
    "JJ2IBblT",
    "JJ6ZWAGR",
    "JJ7HWagR",
    "JJ7XFloA",
    "JJ8HCnrT",
    "KC27swp3",
    "KC2ArolR",
    "KC2IFLYX",
    "LA0ZSLOB",
    "LA1Hfire",
    "LAC8XSln",
    "LV2JscrT",
    "LVXglp01",
    "MN22tctr",
    "MN6XLuckT",
    "NE1YCrsX",
    "NE28RRS1",
    "NE3YbblT",
    "NE6H01",
    "NY23rmV3",
    "NY26RM00",
    "NY7HhoT",
    "NY8Gpt3",
    "OR0HSnap",
    "OR10RLRG",
    "OR36RL01",
    "OR3ZshtZ",
    "OR45RL01",
    "OR4XRp90",
    "OR91FLYX",
    "ORX8rmT2",
    "SF0BlofT",
    "SF0XrazZ",
    "SF1UemTy",
    "SF1YemTy",
    "SF22orc1",
    "SF25olt5",
    "SF28ore2",
    "SF35Hevy",
    "SF3YzipT",
    "SF4XmimA",
    "SF67Swp1",
    "SF6BspoT",
    "SF7XsTop",
    "SF9Zdout",
    "SF9ZflyA",
    "TT10draw",
]

EXPECTED_DEFENSE_BY_SLOT = [
    "NY31RL01",
    "NY31rlNS",
    "CC31rl5m",
    "KCC31rlB",
    "MN31RLD5",
    "MN32RL14",
    "",
    "",
    "DB43rmV0",
    "NY33rmXR",
    "WR33RM1M",
    "KC31rmM",
    "WA33rmR4",
    "Atl3RM22",
    "",
    "",
    "Atl4RR19",
    "OR31RR01",
    "Atl3RR23",
    "Atl3RR27",
    "LV3rr6Bw",
    "SF42RR3S",
    "",
    "",
    "DN23PS06",
    "PEPSB325",
    "SF425PSY",
    "AF31psz3",
    "MN33PS0E",
    "DN23PS11",
    "",
    "",
    "DB32pmR1",
    "SF23PM4C",
    "MN22pmR2",
    "MN32PMM1",
    "MN32pmm4",
    "LV31pmZ3",
    "KC32pmZ2",
    "",
    "KC22plU1",
    "SF23PL6B",
    "AT23PL02",
    "MN31PL02",
    "SF23PL4C",
    "NY3pl1MZ",
    "Atl3PL01",
    "MN31PL02",
    "SF60RDZL",
    "SF43RDR1",
    "GP4RD01",
    "MN33RDR1",
    "KCC3prd6",
    "MN23PD02",
    "MN31PD15",
    "SF22PD7D",
    "",
    "",
    "",
    "",
    "",
    "LACGR34D",
    "WR43RG02",
    "ATF4GLR3",
]

EXPECTED_DEFENSE_BY_NAME = [
    "AF31psz3",
    "AT23PL02",
    "ATF4GLR3",
    "Atl3PL01",
    "Atl3RM22",
    "Atl3RR23",
    "Atl3RR27",
    "Atl4RR19",
    "CC31rl5m",
    "DB32pmR1",
    "DB43rmV0",
    "DN23PS06",
    "DN23PS11",
    "GP4RD01",
    "KC22plU1",
    "KC31rmM",
    "KC32pmZ2",
    "KCC31rlB",
    "KCC3prd6",
    "LACGR34D",
    "LV31pmZ3",
    "LV3rr6Bw",
    "MN22pmR2",
    "MN23PD02",
    "MN31PD15",
    "MN31PL02",
    "MN31PL02",
    "MN31RLD5",
    "MN32PMM1",
    "MN32pmm4",
    "MN32RL14",
    "MN33PS0E",
    "MN33RDR1",
    "NY31RL01",
    "NY31rlNS",
    "NY33rmXR",
    "NY3pl1MZ",
    "OR31RR01",
    "PEPSB325",
    "SF22PD7D",
    "SF23PL4C",
    "SF23PL6B",
    "SF23PM4C",
    "SF425PSY",
    "SF42RR3S",
    "SF43RDR1",
    "SF60RDZL",
    "WA33rmR4",
    "WR33RM1M",
    "WR43RG02",
]


EXPECTED_OFFENSE_CUSTOM_SPECIAL = [
    "BCFGPAT",
    "LACokick",
    "LAC-PUNT",
    "DBONSIDE",
    "",
    "",
    "",
    "",
    "BCFREEK",
    "BCSQUIB",
]

EXPECTED_DEFENSE_CUSTOM_SPECIAL = [
    "",
    "CIN-KR",
    "SKINPRW6",
    "BC-ON-R",
    "SFFKFGRD",
    "SFFFGPas",
    "SFFKPTRD",
    "SFFPuntD",
    "BCFREERT",
    "BCSQUIBR",
]


def test_offense_normal_plays_by_slot() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_normal_plays("slot") == EXPECTED_OFFENSE_BY_SLOT


def test_offense_normal_plays_by_name() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_normal_plays("name") == EXPECTED_OFFENSE_BY_NAME


def test_defense_normal_plays_by_slot() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    assert reader.get_normal_plays("slot") == EXPECTED_DEFENSE_BY_SLOT


def test_defense_normal_plays_by_name() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    assert reader.get_normal_plays("name") == EXPECTED_DEFENSE_BY_NAME


def test_offense_custom_special_plays_in_slot_order() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert reader.get_custom_special_plays() == EXPECTED_OFFENSE_CUSTOM_SPECIAL


def test_defense_custom_special_plays_in_slot_order() -> None:
    reader = GamePlanReader(DEFENSE_PATH)
    assert reader.get_custom_special_plays() == EXPECTED_DEFENSE_CUSTOM_SPECIAL


def test_custom_special_plays_returns_exactly_ten_entries() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    assert len(reader.get_custom_special_plays()) == 10


def test_custom_special_plays_uses_blank_for_empty_slot() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    plays = reader.get_custom_special_plays()
    # Slots 5-8 (indices 4-7) are empty in the offense fixture
    for i in range(4, 8):
        assert plays[i] == ""


# ---------- stream-write methods ----------


def test_write_normal_plays_emits_64_lines_no_header() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out)
    text = out.getvalue()
    assert "===" not in text
    lines = text.splitlines()
    assert len(lines) == 64
    assert lines == EXPECTED_OFFENSE_BY_SLOT


def test_write_normal_plays_honors_sort_name() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out, sort="name")
    assert out.getvalue().splitlines() == EXPECTED_OFFENSE_BY_NAME


def test_write_custom_special_plays_emits_10_lines_no_header() -> None:
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_custom_special_plays(out)
    text = out.getvalue()
    assert "===" not in text
    lines = text.splitlines()
    assert len(lines) == 10
    assert lines == EXPECTED_OFFENSE_CUSTOM_SPECIAL


def test_write_methods_round_trip_via_stringio_then_lines() -> None:
    """Stream-write output is identical to the data accessor + manual join."""
    reader = GamePlanReader(OFFENSE_PATH)
    out = StringIO()
    reader.write_normal_plays(out)
    expected = "\n".join(reader.get_normal_plays()) + "\n"
    assert out.getvalue() == expected
