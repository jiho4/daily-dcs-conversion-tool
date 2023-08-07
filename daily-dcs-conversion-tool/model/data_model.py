# contains parsed data from the input daily text
class ParsedData:
    # store the keywords which exist in this month
    available_keywords = set()

    # dictionaries containing the data of keywords
    # length of dict equals to the size of month
    key_data = dict()  # {date1: {keyword1: sum_num, keyword2: sum_num..}, date2:{}..}
    key_orig_texts = dict()  # {date1: {keyword1: [word1, word2..], keyword2: []..}, date2:{}..}

    # dictionary containing the memo data
    # each date can have several memo lines
    # length of dict equals to the size of month
    memo_data = dict()  # {date1: [memo1, memo2..], date2: []..}


# contains composed data
class OutputData:
    # row_num starts from 0 to the last day of month (0 = header row)
    keyword_part = dict()  # {row_num1: [date1, key1, key1-detail, key2, key2-detail..], row_num2: []..}

    # memo_part has only two columns
    # multiple memo lines can have the same date
    memo_part = []  # [(date, memo), (date, memo)..]
