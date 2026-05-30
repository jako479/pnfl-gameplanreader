# pnfl-gameplanreader — Status

**Status: Complete**

Extracts a list of plays from Front Page Sports Football Pro '98 gameplan (`.pln`) files and emits them as plain text.

## Implemented

- `GamePlanReader` class that lazy-loads a `.pln` via `PnflGamePlan.from_file()` and exposes the 64 normal plays and 10 custom special-teams plays as string lists.
- Slot-order (round-trippable) and name-order (filtered, sorted) output for normal plays.
- `pnfl read-gameplan` CLI registered as a `pnfl` umbrella subcommand, with `--normal-out`, `--special-out`, and `--sort` flags.
- Multiple output modes: human-readable headered stdout, headerless file output, and headerless `-` stdout for piping into `pnfl write-gameplan`.
- CLI-level argument validation (required gameplan path, sort choices, distinct output file paths).
- `PnflGamePlan` binding exposed via `reader.pnfl_gameplan` so consumers that need PNFL-rule validation can opt in without re-loading the file.
- `pnfl check-gameplan` CLI registered as a second `pnfl` umbrella subcommand. Accepts one or more file/directory `PATH`s, with `-r/--recursive` for directory trees. Loads the play pool via `check-gameplan.ini` (`[Settings] PlayPath`) or `--play-path`. Prints a per-file line (`OK (N normal, M custom special)` or violation list with rule, slot, and play details), a summary, and exits `0` clean / `1` violations / `2` usage or I/O error.

## Remaining

- Nothing outstanding for the current scope.
