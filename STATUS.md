# fbpro98-gameplanreader — Status

**Status: Complete**

Extracts a list of plays from Front Page Sports Football Pro '98 gameplan (`.pln`) files and emits them as plain text.

## Implemented

- `GamePlanReader` class that lazy-loads a `.pln` via the shared `fbpro98-gameplan` library and exposes the 64 normal plays and 10 custom special-teams plays as string lists.
- Slot-order (round-trippable) and name-order (filtered, sorted) output for normal plays.
- `pnfl read-gameplan` CLI registered as a `pnfl` umbrella subcommand, with `--normal-out`, `--special-out`, and `--sort` flags.
- Multiple output modes: human-readable headered stdout, headerless file output, and headerless `-` stdout for piping into `pnfl write-gameplan`.
- CLI-level argument validation (required gameplan path, sort choices, distinct output file paths).

## Remaining

- Nothing outstanding for the current scope.
