__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a 
password. The Elves had written the password on a sticky note, but someone threw 
it out.
"""

################################################################################

RANGE_FROM = 138307
RANGE_TO = 654504

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase
    or stay the same (like 111123 or 135679).

    Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

    How many different passwords within the range given in your puzzle input
    meet these criteria?

    The answer should be 1855.
    """

    print(len([password
               for password in range(RANGE_FROM, RANGE_TO + 1)
               if _is_password_valid_1(password)]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    An Elf just remembered one more important detail: the two adjacent matching
    digits are not part of a larger group of matching digits.

    Given this additional criterion, but still ignoring the range rule, the
    following are now true:

    112233 meets these criteria because the digits never decrease and all
    repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger
    group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it
    still contains a double 22).

    How many different passwords within the range given in your puzzle input
    meet all of the criteria?

    The answer should be 1253.
    """

    print(len([password
               for password in range(RANGE_FROM, RANGE_TO + 1)
               if _is_password_valid_2(password)]))

################################################################################

def _is_password_valid_1(password: int) -> bool:
    """
    Checks if the given password is valid:

    -Two adjacent digits are the same (like 22 in 122345).
    -Going from left to right, the digits never decrease; they only ever
     increase or stay the same

    :param password: password to be validated
    :return: True if the password is valid, False otherwise
    """

    password_string = str(password)

    return any([password_string[i] == password_string[i + 1]
                for i in range(len(password_string) - 1)]) \
           and _is_password_increasing_or_same(password)

################################################################################

def _is_password_valid_2(password: int) -> bool:
    """
    Checks if the given password is valid:

    -Two adjacent digits are the same (like 22 in 122345).
    -The two adjacent matching digits are not part of a larger group of matching
     digits.
    -Going from left to right, the digits never decrease; they only ever
     increase or stay the same

    :param password: password to be validated
    :return: True if the password is valid, False otherwise
    """

    password_string = str(password)

    return any([(i == 0
                 and password_string[i] == password_string[i + 1]
                 and password_string[i] != password_string[i + 2])
                or (i >= 1 and i <= len(password_string) - 3
                    and password_string[i] == password_string[i + 1]
                    and password_string[i] != password_string[i + 2]
                    and password_string[i] != password_string[i - 1])
                or (i == len(password_string) - 2
                    and password_string[i] == password_string[i + 1]
                    and password_string[i] != password_string[i - 1])
                for i in range(len(password_string))]) \
           and _is_password_increasing_or_same(password)

################################################################################

def _is_password_increasing_or_same(password: int) -> bool:
    """
    Checks if the given password digits always increase or stay the same going
    left to right.

    :param pasword: password to be validated
    :return: True if the given password digits always increase or stay the same
    going left to right, False otherwise
    """

    password_string = str(password)

    return all([int(password_string[i]) <= int(password_string[i + 1])
                for i in range(len(password_string) - 1)])

################################################################################
