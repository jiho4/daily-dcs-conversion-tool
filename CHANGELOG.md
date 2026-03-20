# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 1.3.0-SNAPSHOT

### Added

- Comprehensive test suite with pytest (33 tests total)
  - `tests/test_util.py`: 14 tests covering all `is_number` cases
  - `tests/test_parse.py`: 19 tests for parsing and validation logic
- Test coverage configuration in `setup.cfg` with XML output
- Enhanced README with detailed input/output format tables, configuration reference, and testing instructions
- Validation for consecutive blank lines after data section initialization

### Changed

- Renamed `input.py` → `reader.py` to avoid shadowing Python's built-in `input()`
- Renamed `print.py` → `writer.py` to avoid shadowing Python's built-in `print()`
- Updated all imports in `__main__.py` to reflect new module names
- Change the output log file unit from daily to yearly
- YAML config loading now uses absolute paths based on `__file__` instead of fragile relative paths
- `print_error_log()` now returns `ValueError` and uses `logger.error()` instead of `print()` and returning `None`
- `csv.writer.writerow('')` replaced with `writerow([])` for proper empty row writing

### Fixed

- Mutable class-level attributes in `ParsedData` and `OutputData` (moved to `__init__` as instance variables)
- `TypeError` from `raise None` when calling `raise print_error_log(...)`
- `IndexError` in `is_number()` when checking empty strings (added early guard check)
- EOF validation false positive when input ended exactly on date `1` line
- Spurious blank row at top of memo output (initialize `current_date` from first entry)
- `line.pop(0)` mutation side effect in `_parse_keyword_line` (use slicing instead)

## [1.2.0] - 2024-09-01

### Added

- Logging configuration and minor fixes

### Fixed

- Import error in util module

## [1.1.0] - 2022-08-07

### Added

- Multi-currency support (JPY, CAD, KRW)
- CSV output with keyword accumulation and memo sections

## [1.1.0] - 2022-06-16

### Added

- Initial release of daily-dcs-conversion-tool
- Core functionality for parsing daily transaction text logs
- CSV output with keyword accumulation and memo sections
- Basic CLI interface with stdin input
