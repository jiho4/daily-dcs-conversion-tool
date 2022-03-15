from enum import Enum, auto


class StrEnum(str, Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self

    def __str__(self):
        return self.name


class Key(StrEnum):
    d = auto()
    f = auto()
    t = auto()
