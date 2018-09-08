"""Contains functions to convert letter-coordiates to numerical coordinates"""

_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
    power =  _num_digits_in_base(number, len(_alphabet)) - 1

    result = ""
    while power >= 0:
        result += _alphabet[number // (len(_alphabet) ** power)]
        number %= (len(_alphabet) ** power)
        power -= 1
    return result


def from_alpha(number: str) -> int:
    """Convert letters to number"""
    assert number
    power = len(number) - 1
    result = 0
    for char in number:
        result += _alphabet.index(char) * (len(_alphabet) ** power)
        power -= 1
    return result
