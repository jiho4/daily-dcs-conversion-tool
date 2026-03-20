# check if it is number (including negative number and float type)
def is_number(s: str) -> bool:
    if not s:
        return False

    # if str starts with '0', treat it as a string (e.g: 0612 is a date)
    # also check length > 1 to avoid treating '0' as a string
    if s[0] == '0' and len(s) > 1:
        return False

    return s.lstrip('-').replace('.', '', 1).isdigit()
