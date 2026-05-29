# pnfl-gameplanreader

Extracts a list of plays from Front Page Sports Football Pro '98 gameplan (`.pln`) files.

Sits on top of [`pnfl-gameplan`](../pnfl-gameplan) (which wraps [`fbpro98-gameplan`](../fbpro98-gameplan) with PNFL rule data). The library handles `.pln` parsing; this project is where CLI behavior and output formats belong.

## Setup

```bash
py -3.13 -m venv .venv
.venv\Scripts\activate
py -m pip install -e ..\fbpro98-gameplan
py -m pip install -e ..\pnfl-playpool
py -m pip install -e ..\pnfl-gameplan
py -m pip install -e ".[dev]"
```

## Usage

Distributed via the [`pnfl`](../pnfl) umbrella CLI:

```bash
pnfl read-gameplan path\to\gameplan.pln
pnfl read-gameplan path\to\gameplan.pln --sort name
pnfl read-gameplan path\to\gameplan.pln --normal-out plays.txt
pnfl read-gameplan path\to\gameplan.pln --normal-out - --special-out -
```

### Output modes

- **Default (no flags)** — both sections to stdout with `=== Normal ===` and `=== Special ===` headers and a blank line between them. Intended for human reading. **Not** consumable by `pnfl write-gameplan`.
- **`--normal-out FILE`** — exactly 64 lines (one per normal slot, blank lines for empty slots), no header.
- **`--special-out FILE`** — exactly 10 lines (one per `special_category`), no header.
- **`-` as FILE** — sends that section to stdout instead of disk. Both flags with `-` produce 74 lines (64 normal + 10 special) on stdout, suitable for piping into `pnfl write-gameplan`.

### Sort order

- `--sort slot` (default) — preserves slot positions; empty slots are blank lines; the file is round-trippable.
- `--sort name` — filters out empty slots and sorts case-insensitively. Variable line count; **not** round-trippable.

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
