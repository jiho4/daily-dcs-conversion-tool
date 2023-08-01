import csv
import os.path
import time

import yaml

with open('resources/config.yml') as f1:
    __conf = yaml.safe_load(f1)


# write output_data into CSV file
def print_text_as_csv(output_data):
    filename = __conf['output_base_filename'] + '-' + time.strftime(__conf['output_filename_time_format']) + '.csv'
    path = __conf['output_directory'] + filename

    # create output directory if it does not exist
    if not os.path.isdir(__conf['output_directory']):
        os.mkdir(__conf['output_directory'])

    with open(path, 'w', encoding='utf-8', newline='') as f2:
        writer = csv.writer(f2, delimiter=__conf['output_delimiter'], quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        # write keyword part first
        _write_keyword_part(writer, output_data.keyword_part)

        # add a simple horizontal rule
        writer.writerow(['====', '========'])

        # write memo part to the below keyword part
        _write_memo_part(writer, output_data.memo_part)


# write keyword part
def _write_keyword_part(writer, keyword_part):
    for row_num in range(0, len(keyword_part)):
        writer.writerow(keyword_part[row_num])


# write memo part
def _write_memo_part(writer, memo_part):
    current_date = 1

    for memo_data_row in memo_part:
        if memo_data_row[0] != current_date:
            # add blank line when date increased
            writer.writerow('')
            current_date = memo_data_row[0]

        writer.writerow(memo_data_row)
