# fbpro98-gameplanreader

Extracts a list of plays from Front Page Sports Football Pro '98 gameplan (`.pln`) files.

Sits on top of the shared [`fbpro98-gameplan`](../fbpro98-gameplan) library rather than
reimplementing the binary `.pln` parser. The library handles file parsing; this project is
where CLI behavior and output formats belong.

## Setup

```bash
py -3.13 -m venv .venv
.venv\Scripts\activate
py -m pip install -e ..\fbpro98-gameplan
py -m pip install -e ".[dev]"
```

## Usage

Distributed via the [`pnfl`](../pnfl) umbrella CLI:

```bash
pnfl read-gameplan path\to\gameplan.pln
pnfl read-gameplan path\to\gameplan.pln --sort name
pnfl read-gameplan path\to\gameplan.pln --output plays.txt
```

Or via module:

```bash
py -m fbpro98_gameplanreader path\to\gameplan.pln
```

Notes:

- `--sort slot` is the default.
- Slot order preserves empty normal-play slots as blank lines.
- `--sort name` emits only actual play names, alphabetized.

## Building a Release

This project is distributed as part of the [`pnfl`](../pnfl) umbrella CLI.
See `pnfl/scripts/build_release.py` for release packaging.

## Testing

```bash
pytest
```

Tests cover:

- offense fixture by slot
- offense fixture by name
- defense fixture by slot
- defense fixture by name
