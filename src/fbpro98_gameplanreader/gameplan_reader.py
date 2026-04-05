from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Literal

from fbpro98_gameplan import GamePlan, read_gameplan

StrPath = str | PathLike[str]
SortOrder = Literal["slot", "name"]


class GamePlanReader:
    def __init__(self, gameplan_path: StrPath) -> None:
        self.gameplan_path = Path(gameplan_path)
        self._gameplan: GamePlan | None = None

    def get_normal_plays(self, sort: SortOrder = "slot") -> list[str]:
        if sort == "slot":
            return self._get_normal_plays_by_slot()
        return sorted(
            (name for name in self._get_normal_plays_by_slot() if name),
            key=str.casefold,
        )

    def _load(self) -> GamePlan:
        if self._gameplan is None:
            self._gameplan = read_gameplan(self.gameplan_path)
        return self._gameplan

    def _get_normal_plays_by_slot(self) -> list[str]:
        gameplan = self._load()
        names: list[str] = []

        for slot in range(gameplan.NUMBER_NORMAL_PLAYS):
            play = gameplan.plays_by_slot.get(slot)
            names.append("" if play is None else play.name)

        return names
