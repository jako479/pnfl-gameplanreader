# TODO

## Pipeline support: stream output to stdout

Allow `--output -` (and `--special-output -`) to write to stdout so output can be piped directly into `pnfl write-gameplan`.

How:
- Treat `-` as a sentinel in `write_output()` meaning "write to stdout."
- When both streams target stdout, emit section headers (`=== Normal Plays ===`, `=== Special Teams ===`) so they're distinguishable; otherwise no headers.

## Special teams export

Add `--special-output FILE` flag and a `get_special_plays(sort)` method on `GamePlanReader` that walks the 20 special-teams slots (slots 64–83). Mirror the normal-plays code path; emit one play name per line in slot order so the file can feed gameplanwriter's special-teams update mode.
