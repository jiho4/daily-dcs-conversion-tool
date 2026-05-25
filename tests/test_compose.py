import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-dcs-conversion-tool'))

from model.data_model import ParsedData, OutputData
from compose import compose_output_text
from util import keys


def _make_parsed_data(key_data, key_orig_texts=None, available_keywords=None, memo_data=None):
    parsed = ParsedData()
    parsed.key_data = key_data
    parsed.key_orig_texts = key_orig_texts or {d: {} for d in key_data}
    parsed.available_keywords = available_keywords or {kw for d in key_data.values() for kw in d}
    parsed.memo_data = memo_data or {d: [] for d in key_data}
    return parsed


# ---------------------------------------------------------------------------
# all_key_data_part
# ---------------------------------------------------------------------------

class TestAllKeyDataPart:
    def test_header_contains_all_keywords(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}},
            key_orig_texts={1: {'e': ['1000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        assert output.all_key_data_part[0] == ['date'] + list(keys.KEYWORDS)

    def test_no_detail_columns_in_header(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}},
            key_orig_texts={1: {'e': ['1000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        header = output.all_key_data_part[0]
        assert not any('-detail' in str(col) for col in header)

    def test_available_keyword_shows_value(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}},
            key_orig_texts={1: {'e': ['1000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        row = output.all_key_data_part[1]
        e_col = output.all_key_data_part[0].index('e')
        assert row[e_col] == 1

    def test_unavailable_keyword_is_blank(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}},
            key_orig_texts={1: {'e': ['1000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        row = output.all_key_data_part[1]
        header = output.all_key_data_part[0]
        for kw in keys.KEYWORDS:
            if kw != 'e':
                assert row[header.index(kw)] == ''

    def test_keyword_missing_on_date_is_blank(self):
        # 'e' exists on date 1 but not date 2
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}, 2: {}},
            key_orig_texts={1: {'e': ['1000']}, 2: {}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        row_date2 = output.all_key_data_part[2]
        e_col = output.all_key_data_part[0].index('e')
        assert row_date2[e_col] == ''

    def test_integer_float_is_stored_as_int(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 2.0}},
            key_orig_texts={1: {'e': ['2000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        row = output.all_key_data_part[1]
        e_col = output.all_key_data_part[0].index('e')
        assert row[e_col] == 2
        assert isinstance(row[e_col], int)

    def test_row_count_equals_num_dates_plus_header(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}, 2: {}, 3: {'e': 2.0}},
            key_orig_texts={1: {'e': ['1000']}, 2: {}, 3: {'e': ['2000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        assert len(output.all_key_data_part) == 4  # header + 3 dates


# ---------------------------------------------------------------------------
# keyword_detail_part
# ---------------------------------------------------------------------------

class TestKeywordDetailPart:
    def test_header_contains_only_available_keywords_with_detail(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}},
            key_orig_texts={1: {'e': ['word1']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        header = output.keyword_detail_part[0]
        assert 'e' in header
        assert 'e-detail' in header
        assert 'ee' not in header
        assert 'ee-detail' not in header

    def test_value_and_detail_are_interleaved(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}},
            key_orig_texts={1: {'e': ['word1', 'word2']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        header = output.keyword_detail_part[0]
        row = output.keyword_detail_part[1]
        assert row[header.index('e')] == 1
        assert row[header.index('e-detail')] == 'word1 word2'

    def test_keyword_missing_on_date_is_blank_in_both_columns(self):
        # 'e' exists on date 1 but not date 2
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}, 2: {}},
            key_orig_texts={1: {'e': ['word1']}, 2: {}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        header = output.keyword_detail_part[0]
        row_date2 = output.keyword_detail_part[2]
        assert row_date2[header.index('e')] == ''
        assert row_date2[header.index('e-detail')] == ''

    def test_row_count_equals_num_dates_plus_header(self):
        parsed = _make_parsed_data(
            key_data={1: {'e': 1.0}, 2: {}, 3: {'e': 2.0}},
            key_orig_texts={1: {'e': ['1000']}, 2: {}, 3: {'e': ['2000']}},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        assert len(output.keyword_detail_part) == 4  # header + 3 dates


# ---------------------------------------------------------------------------
# memo_part
# ---------------------------------------------------------------------------

class TestComposeMemo:
    def test_memo_composed_correctly(self):
        parsed = _make_parsed_data(
            key_data={1: {}},
            memo_data={1: [['memo', 'line']]},
        )
        output = OutputData()
        compose_output_text(parsed, output)

        assert output.memo_part == [(1, 'memo line')]

    def test_empty_memo_data_produces_empty_memo_part(self):
        parsed = _make_parsed_data(key_data={1: {}})
        output = OutputData()
        compose_output_text(parsed, output)

        assert output.memo_part == []
