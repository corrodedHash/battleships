"""Contains functions to convert letter-coordiates to numerical coordinates"""


def to_alpha(number: int) -> str:
    """Convert a number to letters"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    power = 0
    max_num = number // len(alphabet)
    while max_num > 0:
        max_num = max_num // len(alphabet)
        power += 1

    result = ""
    while power >= 0:
        result += alphabet[number // (len(alphabet) ** power)]
        power -= 1
    return result


def from_alpha(number: str) -> int:
    """Convert letters to number"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert number
    power = len(number) - 1
    result = 0
    for char in number:
        result += alphabet.index(char) * (len(alphabet) ** power)
    return result
