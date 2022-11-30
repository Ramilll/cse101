from copy import copy
from typing import Tuple, Union


class Point:
    """Encodes a live point in the Game of Life.
    Data attributes:
    x -- x-coordinate
    y -- y-coordinate
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def neighbor_generator(self):
        """Generates the eight neighbors of a point."""
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                yield Point(self.x + dx, self.y + dy)

    def get_neighbors(self):
        """Return the neighbors of the Point as a set."""
        return set(self.neighbor_generator())


class Board:
    """A board to play the Game of Life on.
    Data attributes:
    alive_points -- a set of Points
    x_size  -- size in x-direction
    y_size  -- size in y-direction
    """

    N_MAX_STEPS = 1000

    def __init__(self, x_size, y_size, points):
        self.x_size = x_size
        self.y_size = y_size
        self.alive_points = set(points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self.x_size == other.x_size and self.y_size == other.y_size and self.alive_points == other.alive_points

    def __hash__(self) -> int:
        return hash((self.x_size, self.y_size, sum(hash(p) for p in self.alive_points)))

    def __repr__(self) -> str:
        return f"Board(x_size={self.x_size}, y_size={self.y_size}, alive_points={self.alive_points})"

    def __copy__(self):
        return Board(self.x_size, self.y_size, self.alive_points.copy())

    def is_legal(self, point):
        """Check if a given Point is on the board."""
        return 0 <= point.x < self.x_size and 0 <= point.y < self.y_size

    def is_point_alive(self, point):
        """Check if a given Point is alive."""
        return point in self.alive_points

    def number_live_neighbors(self, p):
        """Compute the number of live neighbors of p on the Board."""
        return len(self.alive_points.intersection(p.get_neighbors()))

    def number_live_legal_neighbors(self, p):
        """Compute the number of live neighbors of p on the Board."""
        return len([self.is_legal(point) for point in p.get_neighbors()])

    def is_point_present_at_next_step(self, point):
        """Check if a given Point is alive at the next step."""
        if self.is_point_alive(point):
            return 2 <= self.number_live_neighbors(point) <= 3
        else:
            return self.number_live_neighbors(point) == 3

    def next_step(self):
        """Compute the points alive in the next round and update the
        points of the Board.
        """
        next_points = set()
        neighbors = set()
        for point in self.alive_points:
            if self.is_point_alive(point) and self.is_legal(point):
                neighbors.update(point.get_neighbors())
                if self.is_point_present_at_next_step(point):
                    next_points.add(point)

        for point in neighbors:
            if self.is_point_present_at_next_step(point):
                next_points.add(point)

        self.alive_points = next_points

    def toggle_point(self, x, y):
        """Add Point(x,y) if it is not in alive_points, otherwise delete it
        from points.
        """
        point = Point(x, y)
        if point in self.alive_points:
            self.alive_points.remove(point)
        else:
            self.alive_points.add(point)

    def is_periodic(self) -> Union[None, Tuple[bool, int]]:
        """
        Return (True, 0) if the input board is periodic, otherwise (False, i),
        where i is the smallest index of the state to which it loops
        """
        states_by_idx = dict()
        states_by_idx[self] = 0

        next = copy(self)
        print("CURRENT STATE: idx = 0", next)
        for step in range(1, Board.N_MAX_STEPS):
            next.next_step()
            print("NEXT STATE: idx = ", step, next)
            if next in states_by_idx:
                print("END OF THE PROCESS #########", states_by_idx[next])
                return (True, 0) if next == self else (False, step)
            states_by_idx[next] = step


def load_from_file(filename) -> "Board":
    """Load and return a board configuration from file in the following format:
    - The first two lines contain a number representing the size in
        x- and y-coordinates, respectively.
    - Each of the following lines gives the coordinates of a single
        point, with the two coordinate values separated by a comma.
        Those are the points that are alive on the board.
    """
    with open(filename) as f:
        x_size = int(f.readline())
        y_size = int(f.readline())
        points = set()
        for line in f:
            x, y = [int(x) for x in line.split(",")]
            points.add(Point(x, y))
    return Board(x_size, y_size, points)


def is_periodic(board: Board) -> Union[None, Tuple[bool, int]]:
    """Return True if the input board is periodic, otherwise False."""
    return board.is_periodic()
