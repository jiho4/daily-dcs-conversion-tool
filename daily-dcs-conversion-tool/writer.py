import csv
import os
import os.path
import time
from logging import getLogger

import yaml

logger = getLogger(__name__)

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'config.yaml')

with open(_CONFIG_PATH) as f1:
    __conf = yaml.safe_load(f1)


# write output_data into a delimited file
def write_output(output_data):
    filename = __conf['output_base_filename'] + '-' + time.strftime(__conf['output_filename_time_format']) + '.' + __conf['output_file_extension']
    path = __conf['output_directory'] + filename

    # create output directory if it does not exist
    if not os.path.isdir(__conf['output_directory']):
        os.mkdir(__conf['output_directory'])

    with open(path, 'w', encoding='utf-8', newline='') as f2:
        writer = csv.writer(f2, delimiter=__conf['output_delimiter'], quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        # write no-detail part first (all keywords, values only)
        _write_part(writer, output_data.all_key_data_part)

        # add a simple horizontal rule
        writer.writerow(['====', '========'])

        # write keyword-detail part (available keywords with detail)
        _write_part(writer, output_data.keyword_detail_part)

        # add a simple horizontal rule
        writer.writerow(['====', '========'])

        # write memo part
        _write_memo_part(writer, output_data.memo_part)

    logger.info('Output file written: %s', filename)


# write a list of rows
def _write_part(writer, rows):
    for row in rows:
        writer.writerow(row)


# write memo part
def _write_memo_part(writer, memo_part):
    if not memo_part:
        return
    current_date = memo_part[0][0]

    for memo_data_row in memo_part:
        if memo_data_row[0] != current_date:
            # add blank line when date increased
            writer.writerow([])
            current_date = memo_data_row[0]

        writer.writerow(memo_data_row)
