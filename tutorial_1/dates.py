#!/usr/bin/env python3


def hello_world():
    """
    returns 'Hello world!'
    """
    return "Hello world!"


def check_day(n):
    """
    Given an integer between 1 and 7 inclusive,
    return either string 'work!' or string 'rest!'
    depending on whether the day is a workday or not
    """
    if n < 1 or n > 7:
        return None  # invalid m
    elif n <= 5:
        return "work!"
    else:
        return "rest!"


def name_of_month(m):
    """Given an integer m between 1 and 12 inclusive,
    indicating a month of the year, returns the name of that month.
    For example: name_of_month(1) == 'January' and name_of_month(12) == 'December'.
    If the month does not exist (that is, if m is outside the legal range),
    then this function returns None.
    """
    if m < 1 or m > 12:  # Non-existent month
        return None
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return months[m - 1]


def str_with_suffix(n) -> str:
    """Convert the integer n to a string expressing the corresponding
    position in an ordered sequence.
    Eg. 1 becomes '1st', 2 becomes '2nd', etc.
    """
    if n % 10 == 1 and n % 100 != 11:
        return str(n) + "st"
    elif n % 10 == 2 and n % 100 != 12:
        return str(n) + "nd"
    elif n % 10 == 3 and n % 100 != 13:
        return str(n) + "rd"
    else:
        return str(n) + "th"


def is_leap_year(y):
    """Return True if y is a leap year, False otherwise."""
    if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):
        return True
    else:
        return False


def number_of_days(m, y):
    """Returns the number of days in month m of year y."""
    if m < 1 or m > 12:
        return None
    if m == 2:
        if is_leap_year(y):
            return 29
        else:
            return 28
    elif m in [4, 6, 9, 11]:
        return 30
    else:
        return 31


def date_string(d, m, y):
    """Returns a string of the form 'dth mmm yyyy' where d is the day, mmm is the name of the month, and yyyy is the year.
    For example: date_string(1, 1, 2018) == 'The 1st January, 2018'
    """
    if name_of_month(m) is not None and number_of_days(m, y) >= d:
        return f"The {str_with_suffix(d)} of {name_of_month(m)}, {y}"
    else:
        return "Nonexistent date"


def plural(n):
    """adds an ‘s’ to the end of a word if n is not 1"""
    if n == 1:
        return ""
    else:
        return "s"


def time_string(n):
    """which takes a number of seconds n as an argument, and returns a string describing the corresponding
    number of days, hours, minutes, and seconds. time_string always includes a number of seconds in its output
    (even if 0), but ‘0 days’, ‘0 hours’, and ‘0 minutes’ are always omitted."""
    days = n // 86400
    hours = (n % 86400) // 3600
    minutes = (n % 3600) // 60
    seconds = n % 60

    answer = ""
    if days != 0:
        answer += f"{days} day{plural(days)}"
    if hours != 0:
        if answer != "":
            answer += ", "
        answer += f"{hours} hour{plural(hours)}"
    if minutes != 0:
        if answer != "":
            answer += ", "
        answer += f"{minutes} minute{plural(minutes)}"
    if seconds != 0:
        if answer != "":
            answer += ", "
        answer += f"{seconds} second{plural(seconds)}"
    if n == 0:
        return "0 seconds"
    return answer
