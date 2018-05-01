import re

__PATTERN_EMAIL = r'[\w.-]+@\w+.\w+'
__PATTERN_USERNAME_ALLOW_CHARS = r'\w*[\w_-]+\w*'

__SPECIAL_CHARS = ['-', '.', '@', '_', ' ', '#', '$', '=', '/', '*']


def has_uppercase(field: str) -> bool:
    return any(char.isupper() for char in field)


def has_lowercase(field: str) -> bool:
    return any(char.islower() for char in field)


def has_digit(field: str) -> bool:
    return any(char.isdigit() for char in field)


def has_special_char(field: str) -> bool:
    return any(True for char in field if char in __SPECIAL_CHARS)


def is_valid_username(field: str) -> bool:
    return bool(re.fullmatch(__PATTERN_USERNAME_ALLOW_CHARS, field))


def is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(__PATTERN_EMAIL, email))


def check_length(field, start, end):
    return len(field) in range(start, end)


def is_hexadecimal(hexadecimal):
    try:
        int(hexadecimal, 16)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    print(is_hexadecimal('5ae5add4e1382330e8c7bb89'))
