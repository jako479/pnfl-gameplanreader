"""Extract plays from FbPro98 gameplan (.pln) files.

Lazy-loads the underlying GamePlan and exposes the 64 normal plays and 10
custom special-teams plays as plain string lists, with optional sorting.
"""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Literal, TextIO

from fbpro98_gameplan import GamePlan, read_gameplan

StrPath = str | PathLike[str]
SortOrder = Literal["slot", "name"]

NORMAL_HEADER = "=== Normal ==="
SPECIAL_HEADER = "=== Special ==="


class GamePlanReader:
    """Reads a .pln file and exposes its plays as string lists, lazy-loading on first access."""

    def __init__(self, gameplan_path: StrPath) -> None:
        self.gameplan_path = Path(gameplan_path)
        self._gameplan: GamePlan | None = None

    def get_normal_plays(self, sort: SortOrder = "slot") -> list[str]:
        """Return the 64 normal plays.

        With sort="slot" (default), preserves slot positions — empty slots are
        returned as empty strings, so the output is always 64 entries.
        With sort="name", filters out empty slots and sorts case-insensitively
        by play name.
        """
        if sort == "slot":
            return self._get_normal_plays_by_slot()
        return sorted(
            (name for name in self._get_normal_plays_by_slot() if name),
            key=str.casefold,
        )

    def get_custom_special_plays(self) -> list[str]:
        gameplan = self._load()
        return ["" if play is None else play.name for play in gameplan.custom_special_plays]

    def write_normal_plays(self, stream: TextIO, *, sort: SortOrder = "slot") -> None:
        stream.write("\n".join(self.get_normal_plays(sort)) + "\n")

    def write_custom_special_plays(self, stream: TextIO) -> None:
        stream.write("\n".join(self.get_custom_special_plays()) + "\n")

    def _load(self) -> GamePlan:
        if self._gameplan is None:
            self._gameplan = read_gameplan(self.gameplan_path)
        return self._gameplan

    def _get_normal_plays_by_slot(self) -> list[str]:
        gameplan = self._load()
        return ["" if play is None else play.name for play in gameplan.normal_plays]
