def split_type(line):
    """Splits off the first word in the line and returns both parts in a tuple.
    Also eliminates all leading and trailing spaces.
    Example:
        split_type('ROW ##.##') returns ('ROW', '##.##')
        split_type('CLUE (0,1) down: Of or pertaining to the voice (5)') returns
            ('CLUE', '(0,1) down: Of or pertaining to the voice (5)')
        split_type('  ROW    ##.##   ') returns ('ROW', '##.##')

    """
    line = line.strip()
    index = line.find(" ")
    return (line[:index].strip(), line[index + 1 :].strip())


def read_row(row):
    """Reads a row of a crossword puzzle and decomposes it into a list. Every
    '#' is blocking the current box. Letters 'A', ..., 'Z' and 'a', ..., 'z'
    are values that are already filled into the box. These letters are capitalized
    and then put into the list. All other characters stand
    for empty boxes which are represented by a space ' ' in the list.
    Examples:
        read_row('#.#') gives ['#', ' ', '#']
        read_row('C.T') gives ['C', ' ', 'T']
        read_row('cat') gives ['C', 'A', 'T']
    """
    result = []
    for letter in row:
        if letter.isalpha():
            letter = letter.upper()
        elif letter == "#":
            pass
        else:
            letter = " "
        result.append(letter)
    return result


def coord_to_int(coordstring):
    """Reads a coordinate into a couple in the following way: The input is of the form
        '(x,y)' where x, y are integers. The output should then be
        (x, y), where (x, y) is a tuple of values of type int.
    None of these values are strings.
    Example:
        coord_to_int('(0,1)') returns
        (0, 1)
    """
    coordstring = coordstring.strip()
    coordstring = coordstring[1:-1]
    x, y = coordstring.split(",")
    return (int(x), int(y))


def read_clue(cluestring):
    """Reads a clue into a tuple in the following way: The input is of the form
        '(x,y) direction: question (length)'
    where x, y and length are integers, direction is 'across' or 'down'
    and question is the text of the clue. The output should then be
        ((x, y), direction, length, question)
    where (x, y) is a tuple of values of type int and length is of type int.
    There may be arbitrarily many spaces between the different parts of the input.
    Example:
        read_clue('(0,1) down: Of or pertaining to the voice (5)') returns
        ((0, 1), 'down', 5, 'Of or pertaining to the voice')
    """
    cluestring = cluestring.strip()
    coordstring_direction, rest = cluestring.split(":")
    coordstring, direction = coordstring_direction.split()
    coords = coord_to_int(coordstring)
    question, length = rest.split("(")
    length = length[:-1]
    return (coords, direction, int(length), question.strip())


def read_file(filename):
    """Opens the file with the given filename and creates the puzzle in it.
    Returns a pair consisting of the puzzle grid and the list of clues. Assumes
    that the rows and clues are given in this order.
    The description of the rows and clues may interleave arbitrarily.
    """
    with open(filename) as f:
        grid = []
        clues = []
        for line in f:
            line = line.strip()
            if line == "":
                continue
            type, data = split_type(line)
            if type == "ROW":
                grid.append(read_row(data))
            elif type == "CLUE":
                clues.append(read_clue(data))
            else:
                raise ValueError("Unknown type: " + type)
    return (grid, clues)


def create_clue_string(clue):
    """Given a clue, which is a tuple
    (position, direction, length, question),
    create a string in the form 'position direction: question (length)'.
    For example, given the clue
        ((2, 3), 'across', 4, 'Black bird'),
    this function will return
        '(2,3) across: Black bird (4)'
    """
    position, direction, length, question = clue
    x, y = coord_to_int(str(position))
    return f"({x},{y}) {direction}: {question} ({length})"


def create_grid_string(grid):
    """Return a crossword grid as a string."""
    size = len(grid)
    separator = "  +" + ("-----+") * size
    column_number_line = "   "
    column_number_line += "".join(f" {j:2}   " for j in range(size))
    result = f"{column_number_line}\n{separator}\n"
    for (i, row) in enumerate(grid):
        fill = "  |"
        centre_line = f"{i:2}|"
        for entry in row:
            if entry == "#":
                fill += "#####|"
                centre_line += "#####|"
            else:
                fill += "     |"
                centre_line += f"  {entry}  |"
        result += f"{fill}\n{centre_line}\n{fill}\n{separator}\n"
    return result


def create_puzzle_string(grid, clues):
    """Return a human readable string representation of the puzzle."""
    result = create_grid_string(grid)
    result += "\n"
    for clue in clues:
        result += create_clue_string(clue) + "\n"
    return result.rstrip()


def fill_in_word(grid, word, position, direction):
    """Create and return a new grid (a list of lists) based on the grid
    given in the arguments, but with the given word inserted according
    to position and direction.
        - direction: is either 'down' or 'across'.
        - position: the coordinates of the first letter of the word in the grid.
    *This function may modify its grid argument!*
    """
    x, y = position
    if direction == "down":
        for i, letter in enumerate(word):
            grid[x + i][y] = letter
    elif direction == "across":
        for i, letter in enumerate(word):
            grid[x][y + i] = letter
    return grid


def create_row_string(row):
    """Returns a row representation of a string.
    Example:
        create_row_string(['#', 'A', ' ']) returns '#A.'
    """
    return "".join(letter if letter != " " else "." for letter in row)


def compare_two_files(filename1, filename2):
    """Return True if the two files are identical, False otherwise."""
    with open(filename1) as f1, open(filename2) as f2:
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                print(line1, line2, "WRONG")
                return False
    return True


def write_puzzle(filename, grid, clues):
    """Writes the puzzle given by the grid and by the clues to the specified
    file.
    """
    with open(filename, "w") as f:
        for row in grid:
            f.write(f"ROW {create_row_string(row)}\n")
        for clue in clues:
            f.write(f"CLUE {create_clue_string(clue)}\n")
