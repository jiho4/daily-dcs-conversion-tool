import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-dcs-conversion-tool'))

from util.util import is_number


class TestIsNumber:
    # --- cases that should return False ---

    def test_empty_string_returns_false(self):
        assert is_number('') is False

    def test_string_starting_with_zero_returns_false(self):
        assert is_number('0612') is False

    def test_leading_zero_float_returns_false(self):
        assert is_number('0.5') is False

    def test_alphabetic_string_returns_false(self):
        assert is_number('abc') is False

    def test_alphanumeric_string_returns_false(self):
        assert is_number('1a2') is False

    def test_only_dot_returns_false(self):
        assert is_number('.') is False

    def test_only_minus_returns_false(self):
        assert is_number('-') is False

    def test_multiple_dots_returns_false(self):
        assert is_number('1.2.3') is False

    # --- cases that should return True ---

    def test_zero_alone_returns_true(self):
        assert is_number('0') is True

    def test_positive_integer_returns_true(self):
        assert is_number('42') is True

    def test_negative_integer_returns_true(self):
        assert is_number('-10') is True

    def test_positive_float_returns_true(self):
        assert is_number('3.14') is True

    def test_negative_float_returns_true(self):
        assert is_number('-2.5') is True

    def test_large_integer_returns_true(self):
        assert is_number('100000') is True
