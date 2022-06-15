from enum import Enum, auto


# TODO: why not just use tuple instead of enum and manage keywords in config?
class StrEnum(str, Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self

    def __str__(self):
        return self.name


class Keywords(StrEnum):
    d = auto()
    f = auto()
    t = auto()
    u = auto()


class IntKeywords(StrEnum):
    u = auto()