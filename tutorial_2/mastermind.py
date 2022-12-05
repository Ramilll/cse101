import random
from doctest import FAIL_FAST

COLORS = ["RED", "GREEN", "BLUE", "PURPLE", "BROWN", "YELLOW"]


def input_color(color):
    """Return True if the given input color can be found in COLORS
    Use a for-loop to iterate over the list of COLORS.
    """
    for i in range(6):
        if color == COLORS[i]:
            return True
    return False


def create_code():
    """Return 4-element list of strings randomly chosen from
    COLORS with repetition.
    """
    code = []
    for i in range(4):
        code.append(random.choice(COLORS))
    return code


def black_pins(guess, code):
    """guess, code: 4-element lists of strings from COLORS
    Returns the number of black pins, determined by the standard
    Mastermind rules
    """
    black = 0
    for i in range(4):
        if guess[i] == code[i]:
            black += 1
    return black


def create_a_count_dictionary_from_a_list(arr):
    """Return a dictionary with the count of each element in the list"""
    cnt_by_value = {}
    for color in arr:
        if color in cnt_by_value:
            cnt_by_value[color] += 1
        else:
            cnt_by_value[color] = 1
    return cnt_by_value


def count_minimum_number_of_occurences_in_both_dicts(l_dict, r_dict):
    """Return the minimum number of occurences of a color in both dictionaries"""
    min_count = 0
    for color in l_dict:
        if color in r_dict:
            min_count += min(l_dict[color], r_dict[color])
    return min_count


def score_guess(guess, code):
    """guess, code: 4-element lists of strings
    Return (black, white) where
    black is the number of black pins (exact matches), and
    white is the number of white pins (correct colors in wrong places)
    """
    black = black_pins(guess, code)
    cnt_by_color_guess = create_a_count_dictionary_from_a_list(guess)
    cnt_by_color_code = create_a_count_dictionary_from_a_list(code)
    pins = count_minimum_number_of_occurences_in_both_dicts(cnt_by_color_guess, cnt_by_color_code)
    white = pins - black
    return (black, white)


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


def input_guess():
    """Input four colors from COLORS and return as list."""
    user_colors = []
    print("Enter your guess:")

    counter = 1
    while counter <= 4:
        user_color = input(f"{str_with_suffix(counter)} color: ")
        if user_color in COLORS:
            user_colors.append(user_color)
            counter += 1
        else:
            print("Please input a color from the list ['RED', 'GREEN', 'BLUE', 'PURPLE', 'BROWN', 'YELLOW']")
    return user_colors


def one_round(code):
    """Input guess, score guess, print result, and return True iff
    user has won.
    """

    guess = input_guess()
    black, white = score_guess(guess, code)
    print(f"Black pins: {black}, White pins: {white}")
    if black == 4:
        return True
    return False


def play_mastermind(code):
    """Let user guess the code in rounds, use a while-loop"""
    won = False
    cnt_round = 0
    while not won:
        cnt_round += 1
        print("Round", cnt_round)
        won = one_round(code)
    print("You won!")
