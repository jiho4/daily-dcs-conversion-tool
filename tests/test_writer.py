import sys
import os
import io
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'daily-dcs-conversion-tool'))

import writer as writer_module
from model.data_model import OutputData
from writer import _write_part, _write_memo_part, write_output


def _make_dsv_writer():
    buf = io.StringIO()
    w = csv.writer(buf, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    return w, buf


# ---------------------------------------------------------------------------
# _write_part
# ---------------------------------------------------------------------------

class TestWritePart:
    def test_writes_all_rows(self):
        w, buf = _make_dsv_writer()
        _write_part(w, [['date', 'e'], [1, 100], [2, '']])
        lines = buf.getvalue().strip().splitlines()
        assert len(lines) == 3

    def test_empty_rows_writes_nothing(self):
        w, buf = _make_dsv_writer()
        _write_part(w, [])
        assert buf.getvalue() == ''


# ---------------------------------------------------------------------------
# _write_memo_part
# ---------------------------------------------------------------------------

class TestWriteMemoPart:
    def test_writes_memo_rows(self):
        w, buf = _make_dsv_writer()
        _write_memo_part(w, [(1, 'memo line')])
        lines = buf.getvalue().strip().splitlines()
        assert len(lines) == 1

    def test_blank_line_inserted_between_different_dates(self):
        w, buf = _make_dsv_writer()
        _write_memo_part(w, [(1, 'note1'), (2, 'note2')])
        lines = buf.getvalue().splitlines()
        # note1, blank line, note2
        assert len(lines) == 3
        assert lines[1].strip() == ''

    def test_same_date_has_no_blank_line(self):
        w, buf = _make_dsv_writer()
        _write_memo_part(w, [(1, 'note1'), (1, 'note2')])
        lines = buf.getvalue().strip().splitlines()
        assert len(lines) == 2

    def test_empty_memo_writes_nothing(self):
        w, buf = _make_dsv_writer()
        _write_memo_part(w, [])
        assert buf.getvalue() == ''


# ---------------------------------------------------------------------------
# write_output — section order
# ---------------------------------------------------------------------------

class TestWriteOutputSectionOrder:
    def test_section_order(self, tmp_path, monkeypatch):
        # Locate the module-level config dict and redirect output to tmp_path
        conf = next(v for v in vars(writer_module).values()
                    if isinstance(v, dict) and 'output_directory' in v)
        monkeypatch.setitem(conf, 'output_directory', str(tmp_path) + os.sep)

        output_data = OutputData()
        output_data.all_key_data_part = [['date', 'e'], [1, 100]]
        output_data.keyword_detail_part = [['date', 'e', 'e-detail'], [1, 100, 'word']]
        output_data.memo_part = [(1, 'memo')]

        write_output(output_data)

        files = list(tmp_path.glob('*.tsv'))
        assert len(files) == 1
        lines = files[0].read_text(encoding='utf-8').splitlines()

        sep_indices = [i for i, line in enumerate(lines) if '====' in line]
        assert len(sep_indices) == 2
        first_sep, second_sep = sep_indices

        # all_key_data_part header is the first line
        assert 'date' in lines[0]
        # all_key_data_part rows are before the first separator
        assert first_sep > 1
        # keyword_detail_part rows are between the two separators
        assert second_sep > first_sep + 1
        # memo rows are after the second separator
        assert second_sep < len(lines) - 1

    def test_two_separators_written(self, tmp_path, monkeypatch):
        conf = next(v for v in vars(writer_module).values()
                    if isinstance(v, dict) and 'output_directory' in v)
        monkeypatch.setitem(conf, 'output_directory', str(tmp_path) + os.sep)

        output_data = OutputData()
        output_data.all_key_data_part = [['date', 'e'], [1, 100]]
        output_data.keyword_detail_part = [['date', 'e', 'e-detail'], [1, 100, 'word']]
        output_data.memo_part = []

        write_output(output_data)

        lines = list(tmp_path.glob('*.tsv'))[0].read_text(encoding='utf-8').splitlines()
        sep_lines = [line for line in lines if '====' in line]
        assert len(sep_lines) == 2
