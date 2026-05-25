"""
Integration tests: full pipeline from raw input lines to DSV output.
Each test prepares input lines, runs parse → compose → write, reads the
output file back, and compares it line-by-line against the expected output
built with the same dsv writer settings.
"""
import sys
import os
import io
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-dcs-conversion-tool'))

import writer as writer_module
from model.data_model import ParsedData, OutputData
from parse import parse_daily_text
from compose import compose_output_text
from writer import write_output
from util import keywords

TEST_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
SEPARATOR = ['====', '========']


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_pipeline(input_lines, tmp_path, monkeypatch):
    conf = next(v for v in vars(writer_module).values()
                if isinstance(v, dict) and 'output_directory' in v)
    monkeypatch.setitem(conf, 'output_directory', str(tmp_path) + os.sep)
    monkeypatch.setitem(conf, 'output_file_extension', 'csv')

    parsed_data = ParsedData()
    output_data = OutputData()
    parse_daily_text(input_lines, parsed_data, TEST_CONFIG_PATH)
    compose_output_text(parsed_data, output_data)
    write_output(output_data)

    files = list(tmp_path.glob('*.csv'))
    assert len(files) == 1
    return files[0].read_text(encoding='utf-8')


def _build_expected(rows, delimiter='\t'):
    """Serialize rows using the same dsv writer settings."""
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in rows:
        w.writerow(row)
    return buf.getvalue()


def _parse_dsv_lines(content, delimiter='\t'):
    """Parse DSV content into a list of rows (all values as strings)."""
    return list(csv.reader(content.splitlines(), delimiter=delimiter))


def _all_key_row(date, values):
    """Build one data row for all_key_data_part. values: {kw: value}"""
    return [date] + [values.get(kw, '') for kw in keywords.KEYWORDS]


def _detail_row(date, available, values, details):
    """Build one data row for keyword_detail_part.
    available: ordered list of available keywords
    values/details: {kw: value/detail_text}
    """
    row = [date]
    for kw in available:
        row.extend([values.get(kw, ''), details.get(kw, '')])
    return row


# ---------------------------------------------------------------------------
# IT: basic two-day input with three keywords
# ---------------------------------------------------------------------------

class TestBasicTwoDays:
    """
    Input:
        2
        e 2000
        g 1000

        1
        e 1000
        ee 5000

    keywords used: e (date 1 and 2), ee (date 1 only), g (date 2 only)
    digit modifier (jpy default): 4  →  divide by 10^(4-1) = 1000
    """

    INPUT = ['2', 'e 2000', 'g 1000', '', '1', 'e 1000', 'ee 5000', '']

    ALL_KWS = list(keywords.KEYWORDS)
    AVAILABLE = [kw for kw in ALL_KWS if kw in ('e', 'ee', 'g')]

    VALUES  = {1: {'e': 1, 'ee': 5}, 2: {'e': 2, 'g': 1}}
    DETAILS = {1: {'e': '1000', 'ee': '5000'}, 2: {'e': '2000', 'g': '1000'}}

    def _expected_rows(self):
        rows = []
        # all_key_data_part
        rows.append(['date'] + self.ALL_KWS)
        rows.append(_all_key_row(1, self.VALUES[1]))
        rows.append(_all_key_row(2, self.VALUES[2]))
        # separator
        rows.append(SEPARATOR)
        # keyword_detail_part
        rows.append(['date'] + [col for kw in self.AVAILABLE for col in (kw, kw + '-detail')])
        rows.append(_detail_row(1, self.AVAILABLE, self.VALUES[1], self.DETAILS[1]))
        rows.append(_detail_row(2, self.AVAILABLE, self.VALUES[2], self.DETAILS[2]))
        # separator
        rows.append(SEPARATOR)
        return rows

    def test_full_output(self, tmp_path, monkeypatch):
        actual = _run_pipeline(self.INPUT, tmp_path, monkeypatch)
        expected = _build_expected(self._expected_rows())
        # splitlines() normalizes line endings for a portable comparison
        assert actual.splitlines() == expected.splitlines()

    def test_all_key_data_part_header_has_all_keywords(self, tmp_path, monkeypatch):
        actual = _run_pipeline(self.INPUT, tmp_path, monkeypatch)
        header_row = _parse_dsv_lines(actual)[0]
        for kw in keywords.KEYWORDS:
            assert kw in header_row

    def test_keyword_detail_part_only_has_available_keywords(self, tmp_path, monkeypatch):
        actual = _run_pipeline(self.INPUT, tmp_path, monkeypatch)
        lines = actual.splitlines()
        sep_indices = [i for i, l in enumerate(lines) if '====' in l]
        detail_header = next(csv.reader([lines[sep_indices[0] + 1]], delimiter='\t'))

        assert 'e' in detail_header
        assert 'ee' in detail_header
        assert 'g' in detail_header
        for kw in keywords.KEYWORDS:
            if kw not in ('e', 'ee', 'g'):
                assert kw not in detail_header
                assert kw + '-detail' not in detail_header


# ---------------------------------------------------------------------------
# IT: input with memo lines
# ---------------------------------------------------------------------------

class TestWithMemo:
    """
    Input:
        2
        lunch out

        1
        e 3000
        dinner note

    memo on date 2 (lunch out), memo on date 1 (dinner note).
    memo_data is keyed 1 → 2 (insertion order), so date 1 memo comes first.
    """

    INPUT = ['2', 'lunch out', '', '1', 'e 3000', 'dinner note', '']

    ALL_KWS = list(keywords.KEYWORDS)
    AVAILABLE = [kw for kw in ALL_KWS if kw in ('e',)]
    VALUES  = {1: {'e': 3}, 2: {}}
    DETAILS = {1: {'e': '3000'}, 2: {}}

    def _expected_rows(self):
        rows = []
        # all_key_data_part
        rows.append(['date'] + self.ALL_KWS)
        rows.append(_all_key_row(1, self.VALUES[1]))
        rows.append(_all_key_row(2, self.VALUES[2]))
        # separator
        rows.append(SEPARATOR)
        # keyword_detail_part
        rows.append(['date'] + [col for kw in self.AVAILABLE for col in (kw, kw + '-detail')])
        rows.append(_detail_row(1, self.AVAILABLE, self.VALUES[1], self.DETAILS[1]))
        rows.append(_detail_row(2, self.AVAILABLE, self.VALUES[2], self.DETAILS[2]))
        # separator
        rows.append(SEPARATOR)
        # memo: date 1 comes first (inserted first during parse), blank line, then date 2
        rows.append([1, 'dinner note'])
        rows.append([])
        rows.append([2, 'lunch out'])
        return rows

    def test_full_output(self, tmp_path, monkeypatch):
        actual = _run_pipeline(self.INPUT, tmp_path, monkeypatch)
        expected = _build_expected(self._expected_rows())
        assert actual.splitlines() == expected.splitlines()

    def test_memo_section_follows_second_separator(self, tmp_path, monkeypatch):
        actual = _run_pipeline(self.INPUT, tmp_path, monkeypatch)
        lines = actual.splitlines()
        sep_indices = [i for i, l in enumerate(lines) if '====' in l]
        assert len(sep_indices) == 2
        memo_lines = lines[sep_indices[1] + 1:]
        assert any('lunch' in l for l in memo_lines)
        assert any('dinner' in l for l in memo_lines)
