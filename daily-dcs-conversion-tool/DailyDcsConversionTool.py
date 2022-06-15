from collections import deque

import Compose
import Input
import Key
import Parse


class DailyDcsConversionTool:
    # arrays containing the data of keywords
    key_data = dict()
    key_orig_texts = dict()

    # array containing the other data
    other_data = dict()

    # initialize key lists
    for Keyword in Key.Keywords:
        key_data[Keyword.name] = deque([])
        key_orig_texts[Keyword.name] = deque([])

    #################################
    # main TODO: edit the structure of main function
    daily_text = Input.input_string()

    Parse.parse_daily_text(daily_text, key_data, key_orig_texts, other_data)

    Compose.compose_output_text(key_data, key_orig_texts, other_data)

    # Output.print_text