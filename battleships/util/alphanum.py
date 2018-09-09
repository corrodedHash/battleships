"""Contains functions to convert letter-coordiates to numerical coordinates"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _num_digits_in_base(number: int, base: int) -> int:
    """Return amount of digits needed to write the number in the given base"""
    assert number >= 0

    power = 1
    max_num = number // base
    while max_num > 0:
        max_num = max_num // base
        power += 1

    return power


def to_alpha(number: int) -> str:
    """Convert a number to letters"""

    assert number >= 0
    power = _num_digits_in_base(number, len(ALPHABET)) - 1

    result = ""
    while power >= 0:
        result += ALPHABET[number // (len(ALPHABET) ** power)]
        number %= (len(ALPHABET) ** power)
        power -= 1
    return result


def from_alpha(number: str) -> int:
    """Convert letters to number"""
    assert number
    power = len(number) - 1
    result = 0
    for char in number:
        result += ALPHABET.index(char) * (len(ALPHABET) ** power)
        power -= 1
    return result
