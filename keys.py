from enum import Enum

ascii_keys = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0',

    'Q',
    'W',
    'E',
    'R',
    'T',
    'Y',
    'U',
    'I',
    'O',
    'P',

    'A',
    'S',
    'D',
    'F',
    'G',
    'H',
    'J',
    'K',
    'L',

    'Z',
    'X',
    'C',
    'V',
    'B',
    'N',
    'M'
]

pressed = "PRESSED"

class special(str, Enum):
    left_shift = "KEY_LEFTSHIFT"
    right_shift = "KEY_RIGHTSHIFT"
    capslock = "KEY_CAPSLOCK"
    space = "KEY_SPACE"
    tab = "KEY_TAB"
    enter = "KEY_ENTER"
