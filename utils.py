import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.e]$')

def isNumOrDot(string: str) -> bool:
    return bool(NUM_OR_DOT_REGEX.search(string))

def convertToNumber(string: str) -> int | float:
    number = float(string)

    if number.is_integer():
        number = int(number)

    return number

def isValidNumber(string: str) -> bool:
    if string == "e":
        return True
    
    try:
        float(string)
        return True
    except ValueError:
        return False

def isEmpty(string: str) -> bool:
    return len(string) == 0
