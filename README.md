# daily-dcs-conversion-tool

*created: 2022/03/15*

A personal CLI tool that converts daily transaction text logs into formatted delimited reports, designed to speed up end-of-month settlement processing.

---

## Description

This tool parses a month's worth of daily transaction text, accumulates values by keyword and date, and writes the result to a delimited file. It supports multiple currencies and separates transactional data from memo lines in the output. The output delimiter and file extension are configurable (default: tab-separated, `.tsv`).

---

## Requirements

- Python 3.11+
- Dependencies: `PyYAML~=6.0`, `setuptools~=70.0.0`

---

## Getting Started

### Install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python -m daily-dcs-conversion-tool
```

Paste the entire month's daily text into the console, then press `Cmd+D` (macOS/Linux) or `Ctrl+Z` (Windows) to submit.

The tool writes a file to the `output/` directory:

```
output/daily-dcs-converted-YYYY-MM-DD-HHMMSS.tsv
```

The file extension is configurable via `output_file_extension` in `config.yaml`.

---

## Input Format

Input is plain text with the following structure. Dates must appear in **descending order** (last day of month → day 1), separated by blank lines.

```
31
e 5000
g 1200 800
some memo note

30
e 3000
₩e 200
...

1
e 1000

```

**Line types:**

| Type | Example | Description |
|---|---|---|
| Date | `15` | A single integer — the day of the month |
| Keyword | `e 1000` | `<keyword> <value> [value ...]` — values are summed |
| Currency keyword | `₩e 200` | Symbol-prefixed keyword using a different currency |
| Memo | `some note` | Any other text — stored as-is |
| Blank | _(empty)_ | Section separator between dates |

---

## Output Format

The output uses configured delimiter and has three sections separated by `====` horizontal rules:

**Section 1 — All-keyword data** — one row per day, one column per configured keyword (values only, no detail). Keywords with no data appear as blank columns.

| date | e | f | g | ... |
|---|---|---|---|---|
| 1 | 1 | 5 | | |
| 2 | 2 | | 10 | |

**Section 2 — Keyword detail** — one row per day, columns for each keyword that appeared in the input, interleaved with its original text detail. Keywords absent from the input are omitted entirely.

| date | e | e-detail | g | g-detail |
|---|---|---|---|---|
| 1 | 1 | 1000 sample | | |
| 2 | 2 | 2000 detail1 | 1 | 1000 detail2 |

**Section 3 — Memo** — two columns (date, memo text), grouped by date with blank lines between groups. Dates with no memo are omitted:

```
3	some note here

5	another memo
5	second line for day 2
```

---

## Configuration

All settings are in `daily-dcs-conversion-tool/resources/config.yaml`:

| Key | Example | Description |
|---|---|---|
| `default_currency` | `jpy` | Default digit modifier currency |
| `digits` | `{cad: 2, jpy: 4, krw: 5}` | Digit count per currency (used as divisor) |
| `symbols` | `{$: cad, Y: jpy, ¥: jpy, ₩: krw}` | Currency symbol mappings |
| `keywords` | e, f, g, ... | Recognised keyword list |
| `int_keywords` | f, g, ... | Keywords treated as integers |
| `output_directory` | `../output/` | Output file directory |
| `output_delimiter` | `\t` | Column delimiter — escape sequences are supported regardless of YAML quoting style (`"\t"`, `'\t'`, or `\t` all produce a tab) |
| `output_file_extension` | `tsv` | Output file extension |

---

## Development

### Install test dependencies

```bash
pip install -r test_requirements.txt
```

### Run tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov --cov-report=xml    # generates coverage.xml
pytest --cov --cov-report=term   # prints coverage table to terminal
```

---

## Project Structure

```
daily-dcs-conversion-tool/
├── README.md
├── setup.py
├── setup.cfg                    <- pytest and coverage config
├── requirements.txt
├── test_requirements.txt
├── daily-dcs-conversion-tool/
│   ├── __main__.py              <- Entry point, pipeline orchestration
│   ├── reader.py                <- Reads stdin input into line list
│   ├── parse.py                 <- Parses and validates each line
│   ├── compose.py               <- Structures parsed data for output
│   ├── writer.py                <- Writes output as delimited file
│   ├── model/
│   │   ├── data_model.py        <- ParsedData and OutputData classes
│   │   └── line_enum.py         <- LineType enum
│   ├── resources/
│   │   ├── config.yaml          <- Main configuration
│   │   └── log_config.yaml      <- Logging configuration
│   └── util/
│       ├── keywords.py          <- Keyword constants loaded from config
│       └── utils.py             <- Helper functions (is_number)
└── tests/
    ├── test_parse.py
    ├── test_compose.py
    ├── test_writer.py
    ├── test_utils.py
    └── test_integration.py
```
