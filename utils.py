import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.e]$')

def isNumOrDot(string: str) -> bool:
    return bool(NUM_OR_DOT_REGEX.search(string))

def isEmpty(string: str) -> bool:
    return len(string) == 0
