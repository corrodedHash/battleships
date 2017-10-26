
def toAlpha(number):
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

def fromAlpha(number):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert len(number) > 0
    power = len(number) - 1
    result = 0
    for char in number:
        result += alphabet.index(char) * (len(alphabet) ** power)
    return result

