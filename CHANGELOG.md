# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.1.dev0] - Unreleased

### Added

- Added `CALUDE.md` file with a simple development guidelines

### Changed

- Renamed `keys.py`→`keywords.py`, `util.py`→`utils.py`, `test_util.py`→`test_utils.py`, and updated all imports accordingly
- Cleaned up `.gitignore`: removed irrelevant sections and reorganized into simpler categories

### Fixed

- `output_delimiter` in `config.yaml` now works with any YAML quoting style (`"\t"`, `'\t'`, or unquoted `\t`) — escape sequences are decoded after config load
- `IndexError` in `_is_other_currency_line` when `line` is empty or `line[0]` has no keyword after the symbol — added early guard
- `KeyError` in `load_keywords_from_config` when `int_keywords` is absent from config — now returns empty tuple consistent with module-level behaviour
- Logger calls in `print_error_log` changed from string concatenation to lazy `%s` formatting
- Return type annotation on `compose_output_text` corrected from `-> []` to `-> None`
- f-string used consistently for filename construction in `__main__.py` and `writer.py`
- Bare `[]` and `{}` type hints in `parse.py` replaced with `list`, `dict`, and `set`
- `is True` / `is False` comparisons in `_check_validation_of_line` replaced with idiomatic boolean expressions

## [1.4.0] - 2026-04-13 (NOT RELEASED)

### Added

- New `all_key_data_part` output section (first section): all configured keywords as columns, values only, no detail — keywords with no data appear as blank columns rather than being omitted
- Configurable output file extension via `output_file_extension` in `config.yaml` (production default: `tsv`)
- New test suites: `tests/test_compose.py` (13 tests), `tests/test_writer.py` (8 tests), `tests/test_integration.py` (5 end-to-end tests)

### Changed

- Output now has two keyword sections separated by `====` horizontal rules:
  1. All-keyword section (values only, all configured keywords shown)
  2. Keyword-detail section (available keywords only, with original text detail)
- `OutputData.keyword_part` replaced by `all_key_data_part` and `keyword_detail_part` (separate lists of ready-to-print rows)
- `compose.py` now builds keyword-keyed intermediate dicts (`keyword_value`, `keyword_detail`) before composing output rows; `available_keywords` drives which keywords appear in the detail section
- `writer.print_text_as_csv` renamed to `writer.write_output`
- `writer._write_keyword_part` replaced by `writer._write_part` (generic row-list writer)
- Output file extension changed from hardcoded `.csv` to configurable `output_file_extension` (default `tsv`)

### Fixed

- `AttributeError` crash in `parse.py` and `util/keys.py` when `int_keywords` is `null` in config

## [1.3.0] - 2026-03-20

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
