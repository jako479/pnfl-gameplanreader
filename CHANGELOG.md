# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Renamed project and package from `fbpro98-gameplanreader` / `fbpro98_gameplanreader` to `pnfl-gameplanreader` / `pnfl_gameplanreader`. The `pnfl read-gameplan` CLI command name is unchanged.
- `GamePlanReader` now wraps a `PnflGamePlan` internally. New keyword arguments `rules` and `play_pool` accept a PNFL rule set and play pool for callers that need to query PNFL-rule violations via `reader.pnfl_gameplan.validate()`; both default so existing read-only callers do not need to change.
- Dropped direct dependency on `fbpro98-gameplan`. The reader uses `PnflGamePlan`'s `normal_plays` / `custom_special_plays` property forwarders instead of reaching through `.gameplan`.

## [0.1.0] - 2026-05-19

### Added
- Initial gameplan reader CLI with fixture tests.
- CLI parsing tests and logging setup.
- `read-gameplan.bat` launcher.
- `pnfl.commands` entry point for the umbrella CLI.
- Support for custom special plays and stdout output.
- STATUS.md and TEST_STATUS.md documentation.
- Line-ending rules in .editorconfig.

### Changed
- Migrated to the `pnfl` umbrella CLI.
- Migrated to the new gameplan `normal_plays` tuple and `GamePlan` class name.
- Renamed CLI output flags; switched tests to fixture files.
- Standardized project tooling config.
- Cleaned up package `__init__.py`.

### Removed
- `sys.path` hacks from conftest files in favor of editable installs.
