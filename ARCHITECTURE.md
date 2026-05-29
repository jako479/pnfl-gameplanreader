# pnfl-gameplanreader — Architecture

CLI tool that reads a `.pln` gameplan and emits its plays as plain text — to file(s), stdout, or both.

For system-level context, see [pnfl-docs/Design/gameplan-architecture.md](../pnfl-docs/Design/gameplan-architecture.md).

For validation ownership, see [pnfl-docs/Design/gameplan-validation.md](../pnfl-docs/Design/gameplan-validation.md).

## Module layout

```
src/pnfl_gameplanreader/
├── __init__.py
├── cli.py                 # argparse, output dispatch, main()
└── gameplan_reader.py     # GamePlanReader class, get_*/write_* methods
```

## What this package does

- Provides a CLI: `pnfl read-gameplan SRC.pln [--normal-out FILE] [--special-out FILE] [--sort slot|name]`
- Loads a `.pln` via `PnflGamePlan.from_file()` from `pnfl-gameplan` (which delegates to `fbpro98-gameplan.read_gameplan()`)
- Emits plays in two layouts:
  - `--normal-out` (or `-`) → 64 lines, one per normal slot, blanks for empty slots
  - `--special-out` (or `-`) → 10 lines, one per custom-special slot
  - default mode (no flags) → both sections to stdout with `=== Normal ===` / `=== Special ===` headers
- Supports both file paths and `-` for stdout per flag

## PnflGamePlan binding

`GamePlanReader` wraps a `PnflGamePlan` internally. `rules` and `play_pool` are accepted as keyword arguments with defaults: `PNFL_RULES` and an empty `PlayPool`. Extracting play names does not require pool resolution, so the empty default keeps the reader CLI argument-free at the call site. Callers that need PNFL-rule validation against an existing gameplan pass an inhabited pool and call `reader.pnfl_gameplan.validate()`.

## What this package assumes

- The `.pln` file is well-formed (or will fail loudly via `InvalidGamePlanError` from the underlying parser)
- The user only consumes default-mode stdout for human reading; machine-readable output requires the headerless flag modes

## What this package enforces

CLI-level (raise SystemExit):
- `gameplan_path` provided
- `--sort` ∈ {`slot`, `name`}
- Same non-`-` path for both `--normal-out` and `--special-out` rejected

It does **not** validate the `.pln` itself — that responsibility belongs to `fbpro98-gameplan` (structural) and `pnfl-gameplan` (PNFL rules, exposed via `reader.pnfl_gameplan.validate()` when wanted).

## What this package does NOT do

- Parse `.pln` bytes (delegates to `fbpro98-gameplan` via `pnfl-gameplan`)
- Run PNFL-rule validation automatically (exposed via `reader.pnfl_gameplan.validate()` for opt-in callers)
- Modify any file

## Output contract

The headerless modes are the **machine-readable contract**. They are designed to be consumed by `pnfl write-gameplan` directly:

- `--normal-out -` → 64 lines (writer's `--normal-plays -` accepts this)
- `--special-out -` → 10 lines (writer's `--special-plays -` accepts this)
- `--normal-out - --special-out -` → 74 lines (writer accepts via shared stdin source)

The default (with-headers) mode is **human-only**. The writer cannot consume it.

## Testing

- `tests/test_gameplan_reader.py` — `GamePlanReader` class methods against golden text fixtures
- `tests/test_cli.py` — argparse contract and `main()` output for every flag combination, asserted against golden text fixtures

Fixtures live in `tests/data/`:
- `offense.pln` / `defense.pln` — game-produced binary inputs (shared with `fbpro98-gameplan`)
- `expected/` — `.txt` files that pin every output mode for both gameplans
