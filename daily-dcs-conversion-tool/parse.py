from typing import Final

import yaml

from model.line_enum import LineType
from util import keys, util

with open('resources/config.yml') as f:
    __conf = yaml.safe_load(f)

BASE_DIGIT: Final[int] = __conf['base_digit']


# parse a whole text by each line, add data in to parsed_data
def parse_daily_text(daily_text: [], parsed_data):
    # remember the current line of input string
    line_tracker: int = 0

    # current processing date
    current_date: int = 0

    # to control the initialization of the data list
    is_initialized: bool = False

    # remember whether the previous line was blank line or not
    prev_line_was_blank: bool = False

    #####################
    # parse for each line
    for line in daily_text:
        line_tracker += 1

        line = line.split()  # split by whitespace, continuous whitespace is treated as one

        # check if current line is valid
        _check_validation_of_line(line, len(daily_text),
                                  line_tracker, current_date, prev_line_was_blank)

        # get current line type
        line_type: LineType = _find_line_type(line)

        # blank line
        if line_type == LineType.BLANK_LINE:
            prev_line_was_blank = True
            if current_date == 1:  # if last processed date was 1, then end the loop
                break
        # date line
        elif line_type == LineType.DATE_LINE:
            prev_line_was_blank = False
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
            prev_line_was_blank = False
            _parse_keyword_line(line, current_date, BASE_DIGIT, parsed_data.available_keywords,
                                parsed_data.key_data, parsed_data.key_orig_texts)
        # other currency keyword line
        elif line_type == LineType.OTHER_CURRENCY_KEYWORD_LINE:
            prev_line_was_blank = False
            digit_modifier: int = _get_digit_modifier(line[0])
            line[0] = line[0][1:]  # remove symbol (the first letter)
            _parse_keyword_line(line, current_date, digit_modifier, parsed_data.available_keywords,
                                parsed_data.key_data, parsed_data.key_orig_texts)
        # memo line
        elif line_type == LineType.MEMO_LINE:
            prev_line_was_blank = False
            # add to memo_data without any parsing process
            parsed_data.memo_data[current_date].append(line)
        else:
            raise  # TODO: add unexpected line type exception


# check validation and raise an exception when input text data is not valid
def _check_validation_of_line(line: [], num_of_all_line: int, line_tracker: int,
                              current_date: int, prev_line_was_blank: bool):
    if prev_line_was_blank is True and len(line) > 0 and _is_date_line(line) is False:
        raise print_error_log(line, line_tracker, current_date)  # TODO: line after blank line should be date line
    elif line_tracker == num_of_all_line and current_date != 1:
        raise print_error_log(line, line_tracker, current_date)  # TODO: reached EOF but processed date is not 1
    elif _is_date_line(line) is True and current_date != 0 and int(line[0]) != current_date - 1:
        raise print_error_log(line, line_tracker, current_date)  # TODO: date should be decreasing by 1


# find the type of current line
def _find_line_type(line: []) -> LineType:
    if len(line) == 0:
        return LineType.BLANK_LINE
    elif _is_date_line(line):
        return LineType.DATE_LINE
    elif _is_keyword_line(line):
        return LineType.KEYWORD_LINE
    elif _is_other_currency_line(line):
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
def _is_keyword_line(line: []) -> bool:
    if len(line) > 1 and line[0] in keys.KEYWORDS and util.is_number(line[1]):
        return True
    else:
        return False


def _is_other_currency_line(line: []) -> bool:
    symbols = __conf['symbols']
    symbol = line[0][0]
    keyword = line[0][1:]

    if (len(line) > 1 and symbol in symbols
            and keyword in keys.KEYWORDS and util.is_number(line[1])):
        return True
    else:
        return False


# get digit modifier for other currency
def _get_digit_modifier(keyword: str) -> int:
    digits = __conf['digits']
    symbols = __conf['symbols']

    currency = symbols[keyword[0]]
    return digits[currency]


# parse keyword line and put the data into parsed_data
def _parse_keyword_line(line: [], current_date: int, digit_modifier: int,
                        available_keywords: {}, key_data: {}, key_orig_texts: {}):
    keyword = line.pop(0)
    sum_num = 0

    # add keyword to key set to remember that the keyword exists in this month
    available_keywords.add(keyword)

    # add to sum_num until it reaches to the word
    for word in line:
        if util.is_number(word):
            sum_num += float(word)
        else:
            break

    # TODO: if digit modifier != base digit, add that currency symbol as a prefix
    if keyword not in keys.INT_KEYWORDS:
        sum_num /= 10 ** (digit_modifier - 1)  # divide sum by digit_modifier

    # since same keyword lines can exist in the same date
    if keyword not in key_data[current_date]:
        key_data[current_date][keyword] = sum_num
        key_orig_texts[current_date][keyword] = line.copy()
    else:
        key_data[current_date][keyword] += sum_num
        key_orig_texts[current_date][keyword].append("|")
        key_orig_texts[current_date][keyword].extend(line)


# TODO: separate it to error handling py file
# print processing data when error occurred
def print_error_log(line: [], line_tracker: int, current_date: int):
    print("processing line: " + str(line_tracker))
    print("processing date: " + str(current_date))
    print("processing line data: " + ' '.join(line))
