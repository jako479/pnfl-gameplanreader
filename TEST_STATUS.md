# pnfl-gameplanreader — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

### `read-gameplan`

- `GamePlanReader` get/write methods for normal and custom special plays, against golden text fixtures for both offense and defense gameplans.
- Slot-order and name-order sorting, including blank-slot handling and fixed counts (64 normal, 10 special).
- CLI argparse contract: required path, sort choices, `-` stdout token, and rejection of identical output file paths.
- All `main()` output modes — headered stdout, headerless single/combined `-` stdout, file output, and mixed dash/file routing — pinned to fixtures.

### `check-gameplan`

- argparse contract: requires at least one `PATH`, `-r/--recursive` flag, `--config` / `--play-path` defaults.
- `collect_files`: single file, top-level directory glob, recursive tree glob, missing path, wrong-extension file, empty directory, and de-duplication of repeated inputs.
- `check_file`: violation-list output (head line + indented details + play-count summary) and clean output (`OK (N normal, M custom special)`).
- `main`: exit code `0` (clean), `1` (violations found via known-bad fixtures), `2` (missing path); per-directory scanning and the recursive flag.

## Needs tests

- Nothing outstanding for the current scope.
