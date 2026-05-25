# contains parsed data from the input daily text
class ParsedData:
    def __init__(self):
        # store the keywords which exist in this month
        self.available_keywords = set()

        # dictionaries containing the data of keywords
        # length of dict equals to the size of month
        self.key_data = dict()  # {date1: {keyword1: sum_num, keyword2: sum_num...}, date2:{}...}
        self.key_orig_texts = dict()  # {date1: {keyword1: [word1, word2..], keyword2: []...}, date2:{}...}

        # dictionary containing the memo data
        # each date can have several memo lines
        # length of dict equals to the size of month
        self.memo_data = dict()  # {date1: [memo1, memo2...], date2: []...}


# contains composed data
class OutputData:
    def __init__(self):
        # all_key_data_part: all keywords as columns, values only (no detail), including keywords with no data
        self.all_key_data_part = []  # [[header], [date_row], ...] — all keywords, no detail

        # keyword_detail_part: available keywords only, with value and detail columns interleaved
        self.keyword_detail_part = []  # [[header], [date_row], ...] — available keywords + detail

        # memo_part: it has only two columns (date, memo)
        # multiple memo lines can have the same date
        self.memo_part = []  # [(date, memo), (date, memo)...]
