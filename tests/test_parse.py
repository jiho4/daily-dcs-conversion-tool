import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-dcs-conversion-tool'))

import pytest
from model.data_model import ParsedData
from parse import parse_daily_text, _find_line_type, _is_date_line, _is_keyword_line
from model.line_enum import LineType

# Test config path
TEST_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'test_config.yaml')


# ---------------------------------------------------------------------------
# _is_date_line
# ---------------------------------------------------------------------------

class TestIsDateLine:
    def test_single_integer_is_date(self):
        assert _is_date_line(['15']) is True

    def test_single_zero_is_date(self):
        assert _is_date_line(['0']) is True

    def test_two_tokens_is_not_date(self):
        assert _is_date_line(['15', '100']) is False

    def test_non_decimal_is_not_date(self):
        assert _is_date_line(['e']) is False

    def test_empty_line_is_not_date(self):
        assert _is_date_line([]) is False


# ---------------------------------------------------------------------------
# _find_line_type
# ---------------------------------------------------------------------------

class TestFindLineType:
    def test_empty_list_is_blank(self):
        assert _find_line_type([]) == LineType.BLANK_LINE

    def test_single_integer_is_date(self):
        assert _find_line_type(['15']) == LineType.DATE_LINE

    def test_keyword_with_number_is_keyword(self):
        assert _find_line_type(['e', '1000']) == LineType.KEYWORD_LINE

    def test_currency_prefixed_keyword_is_other_currency(self):
        assert _find_line_type(['$e', '200']) == LineType.OTHER_CURRENCY_KEYWORD_LINE

    def test_unknown_text_is_memo(self):
        assert _find_line_type(['some', 'note', 'here']) == LineType.MEMO_LINE


# ---------------------------------------------------------------------------
# parse_daily_text — happy path
# ---------------------------------------------------------------------------

class TestParseDailyText:
    def _make_input(self, *lines):
        return list(lines)

    def test_single_day_single_keyword(self):
        lines = self._make_input('1', 'e 1000', '')
        parsed = ParsedData()
        parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

        assert 'e' in parsed.available_keywords
        assert parsed.key_data[1]['e'] == pytest.approx(1.0)  # 1000 / 10^(4-1) = 1.0

    def test_multiple_days(self):
        lines = self._make_input('2', 'e 2000', '', '1', 'e 1000', '')
        parsed = ParsedData()
        parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

        assert parsed.key_data[2]['e'] == pytest.approx(2.0)  # 2000 / 1000
        assert parsed.key_data[1]['e'] == pytest.approx(1.0)  # 1000 / 1000

    def test_same_keyword_same_day_is_accumulated(self):
        lines = self._make_input('1', 'e 1000', 'e 2000', '')
        parsed = ParsedData()
        parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

        assert parsed.key_data[1]['e'] == pytest.approx(3.0)  # (1000 + 2000) / 1000

    def test_memo_line_stored(self):
        lines = self._make_input('1', 'some memo note', '')
        parsed = ParsedData()
        parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

        assert len(parsed.memo_data[1]) == 1
        assert parsed.memo_data[1][0] == ['some', 'memo', 'note']

    def test_int_keyword_not_divided(self):
        lines = self._make_input('1', 'u 5', '')
        parsed = ParsedData()
        parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

        # int_keywords are not divided by digit_modifier
        assert parsed.key_data[1]['u'] == pytest.approx(5.0)

    # ---------------------------------------------------------------------------
    # parse_daily_text — blank line rules (from test_drafts.txt)
    # ---------------------------------------------------------------------------

    def test_consecutive_blank_lines_before_initialized_are_accepted(self):
        lines = self._make_input('', '', '1', 'e 1000', '')
        parsed = ParsedData()
        parse_daily_text(lines, parsed, TEST_CONFIG_PATH)  # should not raise

    def test_consecutive_blank_lines_after_initialized_raises(self):
        lines = self._make_input('2', 'e 1000', '', '', '1', 'e 500', '')
        parsed = ParsedData()
        with pytest.raises(ValueError):
            parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

    # ---------------------------------------------------------------------------
    # parse_daily_text — validation errors
    # ---------------------------------------------------------------------------

    def test_non_date_line_after_blank_raises(self):
        lines = self._make_input('2', 'e 1000', '', 'not a date', '')
        parsed = ParsedData()
        with pytest.raises(ValueError):
            parse_daily_text(lines, parsed, TEST_CONFIG_PATH)

    def test_non_sequential_date_raises(self):
        lines = self._make_input('3', 'e 1000', '', '1', 'e 500', '')
        parsed = ParsedData()
        with pytest.raises(ValueError):
            parse_daily_text(lines, parsed, TEST_CONFIG_PATH)
