# check if it is number (including negative number and float type)
def is_number(s: str) -> bool:
    # if str starts with '0', treat it as a string (e.g: 0612 is a date)
    if s[0] == '0':
        return False

    return s.lstrip('-').replace('.', '', 1).isdigit()
