# pnfl-gameplanreader

Two CLI commands over Front Page Sports Football Pro '98 gameplan (`.pln`) files. Sits on [`pnfl-gameplan`](../pnfl-gameplan).

- `pnfl read-gameplan` — extract the play lists from a `.pln`.
- `pnfl check-gameplan` — validate one or more `.pln` files against the PNFL rule set.

## Setup

```bash
py -3.13 -m venv .venv
.venv\Scripts\activate
py -m pip install -e ..\fbpro98-gameplan -e ..\pnfl-playpool -e ..\pnfl-gameplan -e ".[dev]"
```

## `read-gameplan`

```bash
pnfl read-gameplan gameplan.pln                              # both sections to stdout, headered
pnfl read-gameplan gameplan.pln --sort name                  # name-sorted normal plays
pnfl read-gameplan gameplan.pln --normal-out plays.txt       # 64 lines to file, no header
pnfl read-gameplan gameplan.pln --normal-out - --special-out -  # 74 lines to stdout, pipeable to write-gameplan
```

- Default (no flags): headered stdout, human-only — **not** consumable by `write-gameplan`.
- `--normal-out` / `--special-out FILE`: headerless 64 / 10 lines. `-` means stdout. Both flags with `-` together → 74 lines suitable for piping into `pnfl write-gameplan`.
- `--sort slot` (default): preserves positions, round-trippable. `--sort name`: filtered + sorted, variable length, not round-trippable.

## `check-gameplan`

```bash
pnfl check-gameplan gameplan.pln
pnfl check-gameplan Off1.pln Off2.pln Def1.pln Def2.pln
pnfl check-gameplan path\to\directory [-r]
```

Each `PATH` is a `.pln` file, directory (top-level scan; `-r` for tree), or glob (expanded internally). Play pool from `check-gameplan.ini` `[Settings] PlayPath` (same lookup as `write-gameplan.ini`) or `--play-path DIR`.

Per-file output:

```
Off1.pln: OK (60 normal, 6 custom special)
Off2.pln: 2 violation(s) (58 normal, 5 custom special)
  [PSL] Offensive category 'PSL' has 4 plays; PNFL requires at least 5.
  Duplicate play 'OR45RL01' at slot 5 (2-1) (already at slot 1 (1-1))

4 file(s) checked, 2 violation(s) across 1 file(s).
```

Exit codes: `0` clean, `1` violations found, `2` usage / I/O error.

## Building a Release

Ships these artifacts to the umbrella bundle:

- `release/read-gameplan.bat` — launcher template
- Python wheel (built by `pnfl/scripts/build_release.py`)

Distributed as part of the [`pnfl`](../pnfl) umbrella CLI.

## Testing

```bash
pytest
```

Cross-CLI pipeline tests (`read-gameplan` → `write-gameplan`) live in [`pnfl/tests/test_gameplan.py`](../pnfl/tests/test_gameplan.py).
