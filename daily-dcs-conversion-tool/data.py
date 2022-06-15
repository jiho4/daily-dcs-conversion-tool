from collections import deque
import key


class Data:
    # arrays containing the data of keywords
    key_data = dict()
    key_orig_texts = dict()

    # initialize key lists
    for keyword in key.KEYWORDS:
        key_data[keyword] = deque([])
        key_orig_texts[keyword] = deque([])

    # array containing the other data
    other_data = dict()

    # the last day of this month
    last_day: int = -1
