# fbpro98-gameplanreader

`fbpro98-gameplanreader` extracts a list of plays from Front Page Sports Football Pro '98
gameplan (`.pln`) files.

The project is intended to sit on top of the shared
[`fbpro98-gameplan`](../fbpro98-gameplan) library rather than reimplementing the
binary `.pln` parser. The library handles file parsing; this project is where
CLI behavior and output formats belong.

## Current Scope

The current tool:

- loads a `.pln` file through `fbpro98-gameplan`
- lists the normal plays in the gameplan
- supports slot order or alphabetical order
- writes to the console by default or to a text file with `--output`

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

Install the sibling library into this environment first:

```bash
pip install -e ..\fbpro98-gameplan
```

Then install this project, with dev dependencies if needed:

```bash
pip install -e ".[dev]"
```

Why the editable installs matter:

- `fbpro98-gameplanreader` depends on the sibling `fbpro98-gameplan` package.
- `-e` means changes in either repo are picked up immediately without reinstalling after each edit.

## Usage

Console output:

```bash
python -m fbpro98_gameplanreader path\to\gameplan.pln
```

Sort by name instead of slot:

```bash
python -m fbpro98_gameplanreader path\to\gameplan.pln --sort name
```

Write output to a text file:

```bash
python -m fbpro98_gameplanreader path\to\gameplan.pln --output plays.txt
```

Notes:

- `--sort slot` is the default.
- Slot order preserves empty normal-play slots as blank lines.
- `--sort name` emits only actual play names, alphabetized.

## Testing

Run:

```bash
pytest
```

The tests cover:

- offense fixture by slot
- offense fixture by name
- defense fixture by slot
- defense fixture by name

## Development Notes

- Keep `.pln` binary parsing in `fbpro98-gameplan`.
- Keep this repo focused on orchestration, filtering, and output concerns.
- If multiple output targets are added, they should sit behind a small writer/output abstraction rather than being mixed into the CLI entry point.
