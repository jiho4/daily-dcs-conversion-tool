# daily-dcs-conversion-tool

*created: 2022/03/15*

A personal CLI tool that converts daily transaction text logs into formatted CSV reports, designed to speed up end-of-month settlement processing.

---

## Description

This tool parses a month's worth of daily transaction text, accumulates values by keyword and date, and writes the result to a tab-separated CSV file. It supports multiple currencies and separates transactional data from memo lines in the output.

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

The tool writes a CSV file to the `output/` directory:

```
output/daily-dcs-converted-YYYY-MM-DD-HHMMSS.csv
```

---

## Input Format

Input is plain text with the following structure. Dates must appear in **descending order** (last day of month → day 1), separated by blank lines.

```
31
e 5000
sv 1200 800
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

The CSV uses tab (`\t`) as delimiter and has two sections:

**Keyword part** — one row per day, columns for each keyword's sum and original text detail:

| date | e | e-detail | sv | sv-detail | ... |
|---|---|---|---|---|---|
| 1 | 1.0 | 1000 | | | |
| 2 | 3.5 | 2000 1500 | 2.0 | 1200 800 | |

**Memo part** — two columns (date, memo text), grouped by date with blank lines between groups:

```
1	some note here
2	another memo
2	second line for day 2
```

---

## Configuration

All settings are in `daily-dcs-conversion-tool/resources/config.yaml`:

| Key | Default | Description |
|---|---|---|
| `default_currency` | `jpy` | Default digit modifier currency |
| `digits` | `{cad: 2, jpy: 4, krw: 5}` | Digit count per currency (used as divisor) |
| `symbols` | `{$: cad, Y: jpy, ¥: jpy, ₩: krw}` | Currency symbol mappings |
| `keywords` | _(28 entries)_ | Recognised keyword list |
| `int_keywords` | `u, z, j` | Keywords treated as integers (not divided) |
| `output_directory` | `../output/` | Output CSV directory |
| `output_delimiter` | `\t` | CSV column delimiter |

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
│   ├── writer.py                <- Writes output as CSV
│   ├── model/
│   │   ├── data_model.py        <- ParsedData and OutputData classes
│   │   └── line_enum.py         <- LineType enum
│   ├── resources/
│   │   ├── config.yaml          <- Main configuration
│   │   └── log_config.yaml      <- Logging configuration
│   └── util/
│       ├── keys.py              <- Keyword constants loaded from config
│       └── util.py              <- Helper functions (is_number)
└── tests/
    ├── test_parse.py
    └── test_util.py
```
