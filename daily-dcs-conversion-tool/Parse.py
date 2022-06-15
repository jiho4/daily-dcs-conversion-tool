from typing import Final
import Key
import yaml

with open('resources/config.yml') as f:
    conf = yaml.safe_load(f)


def parse_daily_text(daily_text: [], key_data: dict(), key_orig_texts: dict(), other_data: dict()):
    # remember the current line of input string
    line_tracker: int = 0

    # the last day of this month
    last_day: int = -1  # TODO: do I need it?

    # current processing date
    current_date: int = 0

    # remember whether the previous line was blank line or not
    prev_line_was_blank: bool = False

    #####################
    # parse for each line
    for line in daily_text:
        line_tracker += 1

        line = line.split()  # split by whitespace, continuous whitespace is treated as one

        print("for line: " + ' '.join(line))  # TODO: remove it after test

        # check if current line is valid
        check_validation_of_line(line, len(daily_text), line_tracker, current_date, prev_line_was_blank)

        # blank line
        if len(line) == 0:
            prev_line_was_blank = True
            if current_date == 1:  # if last processed date was 1, then end the loop
                break
        else:
            prev_line_was_blank = False

        # date line
        if is_date_line(line):
            current_date = int(line[0])

            if last_day == -1:  # update only once
                last_day = int(line[0])
                for i in range(0, last_day):
                    other_data[i] = []

        # keyword line
        elif is_keyword_line(line):
            parse_keyword_line(line, key_data, key_orig_texts)
        # memo lines
        else:
            other_data[current_date] = line


def check_validation_of_line(line: [], num_of_all_line: int, line_tracker: int
                             , current_date: int, prev_line_was_blank: bool):
    if prev_line_was_blank is True and is_date_line(line) is False:
        raise  # TODO: line after blank line should be date line
    elif line_tracker == num_of_all_line and current_date != 1:
        raise  # TODO: reached EOF but processed date is not 1
    elif is_date_line(line) is True and int(line[0]) == current_date - 1:
        raise  # TODO: date should be decreasing by 1


def is_date_line(line: []) -> bool:
    if len(line) == 1 and line[0].isdecimal():
        return True
    else:
        return False


def is_keyword_line(line: []) -> bool:
    if len(line) > 1 and line[0] in Key.Keywords.__members__ and is_number(line[1]):
        return True
    else:
        return False


def parse_keyword_line(line: [], key_data: [], key_orig_texts: []):
    # digit modifier for current currency
    base_digit: Final = conf['base_digit']

    keyword = line.pop(0)
    sum_num = 0

    for word in line:
        if is_number(word):
            sum_num += float(word)

    if keyword not in Key.IntKeywords.__members__:
        sum_num /= 10 ** (base_digit - 1)  # divide sum by base digit

    key_data[keyword].appendleft(sum_num)
    key_orig_texts[keyword].appendleft(line)


# check if it is number (including negative number and float type)
def is_number(s: str) -> bool:
    return s.lstrip('-').replace('.', '', 1).isdigit()


# TODO: separate it to error handling py file
# print processing data when error occurred
def print_error_log(line: [], line_tracker: int, current_date: int):
    print("processing line: " + line_tracker)
    print("processing date: " + current_date)
    print("processing line data: " + line)
