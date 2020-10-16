import random
import string


def get_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))

    return result_str


def to_fixed(number, digits=0):
    return f'{number:.{digits}f}'
