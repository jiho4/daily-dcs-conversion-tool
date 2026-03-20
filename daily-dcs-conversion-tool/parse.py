import os
from logging import getLogger
from typing import Final, Optional

import yaml

from model.line_enum import LineType
from util import keys, util

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'config.yaml')

with open(_CONFIG_PATH) as f:
    __conf = yaml.safe_load(f)

BASE_DIGIT: Final[int] = __conf['digits'][__conf['default_currency']]

logger = getLogger(__name__)


def _load_config(config_path: str):
    """Load config from a specific path."""
    with open(config_path) as f:
        return yaml.safe_load(f)


# parse a whole text by each line, add data in to parsed_data
def parse_daily_text(daily_text: [], parsed_data, config_path: Optional[str] = None):
    # Load config
    conf = _load_config(config_path) if config_path else __conf
    base_digit = conf['digits'][conf['default_currency']]
    keywords = tuple(conf['keywords'].split(', '))
    int_keywords = tuple(conf['int_keywords'].split(', '))

    # remember the current line of input string
    line_tracker: int = 0

    # current processing date
    current_date: int = 0

    # to control the initialization of the data list
    is_initialized: bool = False

    # remember whether the previous line was blank line or not
    was_prev_line_blank: bool = False

    #####################
    # parse for each line
    for line in daily_text:
        line_tracker += 1

        line = line.split()  # split by whitespace, continuous whitespace is treated as one

        # check if current line is valid
        _check_validation_of_line(line, len(daily_text),
                                  line_tracker, current_date, was_prev_line_blank, is_initialized)

        # get current line type
        line_type: LineType = _find_line_type(line, conf, keywords)

        # blank line
        if line_type == LineType.BLANK_LINE:
            was_prev_line_blank = True
            if current_date == 1:  # if last processed date was 1, then end the loop
                break
        # date line
        elif line_type == LineType.DATE_LINE:
            was_prev_line_blank = False
            current_date = int(line[0])

            if is_initialized is False:  # run only once
                # initialize data lists, as size equals to the last day of month
                for i in range(1, int(line[0]) + 1):
                    parsed_data.key_data[i] = dict()
                    parsed_data.key_orig_texts[i] = dict()
                    parsed_data.memo_data[i] = []
                is_initialized = True
        # keyword line
        elif line_type == LineType.KEYWORD_LINE:
            was_prev_line_blank = False
            _parse_keyword_line(line, current_date, base_digit, parsed_data.available_keywords,
                                parsed_data.key_data, parsed_data.key_orig_texts, int_keywords)
        # other currency keyword line
        elif line_type == LineType.OTHER_CURRENCY_KEYWORD_LINE:
            was_prev_line_blank = False
            digit_modifier: int = _get_digit_modifier(line[0], conf)
            line[0] = line[0][1:]  # remove symbol (the first letter)
            _parse_keyword_line(line, current_date, digit_modifier, parsed_data.available_keywords,
                                parsed_data.key_data, parsed_data.key_orig_texts, int_keywords)
        # memo line
        elif line_type == LineType.MEMO_LINE:
            was_prev_line_blank = False
            # add to memo_data without any parsing process
            parsed_data.memo_data[current_date].append(line)
        else:
            raise ValueError("Unexpected line type")


# check validation and raise an exception when input text data is not valid
def _check_validation_of_line(line: [], num_of_all_line: int, line_tracker: int,
                              current_date: int, was_prev_line_blank: bool, is_initialized: bool):
    if was_prev_line_blank is True and is_initialized is True and len(line) == 0:
        raise print_error_log(line, line_tracker, current_date, "consecutive blank lines after init not allowed")
    elif was_prev_line_blank is True and len(line) > 0 and _is_date_line(line) is False:
        raise print_error_log(line, line_tracker, current_date, "line after blank line should be date line")
    elif line_tracker == num_of_all_line and current_date != 1 and not (_is_date_line(line) and int(line[0]) == 1):
        raise print_error_log(line, line_tracker, current_date, "reached EOF but processed date is not 1")
    elif _is_date_line(line) is True and current_date != 0 and int(line[0]) != current_date - 1:
        raise print_error_log(line, line_tracker, current_date, "date should be decreasing by 1")


# find the type of current line
def _find_line_type(line: [], conf=None, keywords=None) -> LineType:
    if conf is None:
        conf = __conf
    if keywords is None:
        keywords = keys.KEYWORDS

    if len(line) == 0:
        return LineType.BLANK_LINE
    elif _is_date_line(line):
        return LineType.DATE_LINE
    elif _is_keyword_line(line, keywords):
        return LineType.KEYWORD_LINE
    elif _is_other_currency_line(line, conf, keywords):
        return LineType.OTHER_CURRENCY_KEYWORD_LINE
    else:
        return LineType.MEMO_LINE


# check if current line is a date line
def _is_date_line(line: []) -> bool:
    if len(line) == 1 and line[0].isdecimal():
        return True
    else:
        return False


# check if current line is a keyword line
def _is_keyword_line(line: [], keywords=None) -> bool:
    if keywords is None:
        keywords = keys.KEYWORDS
    if len(line) > 1 and line[0] in keywords and util.is_number(line[1]):
        return True
    else:
        return False


def _is_other_currency_line(line: [], conf=None, keywords=None) -> bool:
    if conf is None:
        conf = __conf
    if keywords is None:
        keywords = keys.KEYWORDS

    symbols = conf['symbols']
    symbol = line[0][0]
    keyword = line[0][1:]

    if (len(line) > 1 and symbol in symbols
            and keyword in keywords and util.is_number(line[1])):
        return True
    else:
        return False


# get digit modifier for other currency
def _get_digit_modifier(keyword: str, conf=None) -> int:
    if conf is None:
        conf = __conf

    digits = conf['digits']
    symbols = conf['symbols']

    currency = symbols[keyword[0]]
    return digits[currency]


# parse keyword line and put the data into parsed_data
def _parse_keyword_line(line: [], current_date: int, digit_modifier: int,
                        available_keywords: {}, key_data: {}, key_orig_texts: {}, int_keywords=None):
    if int_keywords is None:
        int_keywords = keys.INT_KEYWORDS

    keyword = line[0]
    line = line[1:]
    sum_num = 0

    # add keyword to key set to remember that the keyword exists in this month
    available_keywords.add(keyword)

    # add to sum_num until it reaches to the word
    for word in line:
        if util.is_number(word):
            sum_num += float(word)
        else:
            break

    if keyword not in int_keywords:
        sum_num /= 10 ** (digit_modifier - 1)  # divide sum by digit_modifier

    # since same keyword lines can exist in the same date
    if keyword not in key_data[current_date]:
        key_data[current_date][keyword] = sum_num
        key_orig_texts[current_date][keyword] = line.copy()
    else:
        key_data[current_date][keyword] += sum_num
        key_orig_texts[current_date][keyword].append("|")
        key_orig_texts[current_date][keyword].extend(line)


# print processing data when error occurred and return an exception to raise
def print_error_log(line: [], line_tracker: int, current_date: int, message: str) -> ValueError:
    logger.error("processing line: " + str(line_tracker))
    logger.error("processing date: " + str(current_date))
    logger.error("processing line data: " + ' '.join(line))
    logger.error("error reason: " + message)
    return ValueError("Invalid input at line {}: {} - {}".format(line_tracker, ' '.join(line), message))
