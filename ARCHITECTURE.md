# pnfl-gameplanreader — Architecture

Hosts two CLIs over `.pln` gameplans. See [pnfl-docs/Design/gameplan-architecture.md](../pnfl-docs/Design/gameplan-architecture.md) for system context and [gameplan-validation.md](../pnfl-docs/Design/gameplan-validation.md) for validation ownership.

## Module layout

```
src/pnfl_gameplanreader/
├── reader_cli.py          # read-gameplan: argparse, output dispatch, main()
├── check_cli.py           # check-gameplan: file collection, validate loop, main()
├── config.py              # Config + INI lookup (check-gameplan only)
└── gameplan_reader.py     # GamePlanReader: get_*/write_* methods
```

## `read-gameplan`

`GamePlanReader` wraps a lazy-loaded `PnflGamePlan`. `rules` defaults to `PNFL_RULES` and `play_pool` defaults to an empty `PlayPool` — extracting play names doesn't need pool resolution. Callers that want validation pass an inhabited pool and call `reader.pnfl_gameplan.validate()`.

Output modes:

- Default (no flags): both sections to stdout with `=== Normal ===` / `=== Special ===` headers — **human-only**, not consumable by `write-gameplan`.
- `--normal-out FILE|-`: 64 lines, headerless (blanks for empty slots).
- `--special-out FILE|-`: 10 lines, headerless.
- Both with `-`: 74 lines on stdout, piped straight into `write-gameplan`.

`--sort slot` (default) preserves positions and round-trips; `--sort name` filters empty slots and sorts case-insensitively.

## `check-gameplan`

`check_cli.main` walks each `PATH` (file, directory, or glob; `-r` recurses directories). For each, `PnflGamePlan.from_file(path, PNFL_RULES, play_pool)` + `.validate()`. Per-file output, see [README.md](README.md#check-gameplan). Exit `0` clean, `1` violations, `2` usage/I/O.

Play pool comes from `check-gameplan.ini` `[Settings] PlayPath` (cwd or `cwd/config/`) or `--play-path DIR`. Defaults to `C:\SIERRA\FbPro98\PNFL`.

## Testing

- `tests/test_gameplan_reader.py` — `GamePlanReader` methods against golden text fixtures.
- `tests/test_reader_cli.py` — `read-gameplan` argparse and `main()` output for every flag combination.
- `tests/test_check_cli.py` — `check-gameplan` argparse, `collect_files` (file/dir/recursive/glob/dedupe), `check_file` output, `main()` exit codes. Clean-file output uses `monkeypatch` since both fixtures have known violations.

Fixtures in `tests/data/`: `offense.pln`, `defense.pln`, plus `expected/` `.txt` files pinning every `read-gameplan` output mode.
