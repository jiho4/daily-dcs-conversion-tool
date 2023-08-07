from enum import Enum, auto


class LineType(Enum):
    BLANK_LINE = auto()
    DATE_LINE = auto()
    KEYWORD_LINE = auto()
    OTHER_CURRENCY_KEYWORD_LINE = auto()
    MEMO_LINE = auto()
