# check if it is number (including negative number and float type)
def is_number(s: str) -> bool:
    return s.lstrip('-').replace('.', '', 1).isdigit()
