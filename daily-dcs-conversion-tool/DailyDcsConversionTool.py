from typing import Final
import Input
import Key


class DailyDcsConversionTool:
    # digit modifier for current currency
    BASE_DIGIT: Final = 4

    # remember the current line of input string
    lineTracker = 0

    # the last day of this month
    lastDay: Final

    # current processing date
    currentDate = 0

    # arrays containing the data of keywords
    keyData = [None] * len(Key.Key)
    keyOrigTexts = [None] * len(Key.Key)

    # array containing the other data
    etcData = []

    # main TODO: edit the structure of main function
    dailyText = Input.input_string()

    print(dailyText)