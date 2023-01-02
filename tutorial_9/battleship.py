import random
from typing import List, Set, Tuple, Union

ship_types = [("Battleship", 4), ("Carrier", 5), ("Cruiser", 3), ("Destroyer", 2), ("Submarine", 3)]


class Ship:
    """A ship that can be placed on the grid."""

    def __init__(self, name: str, positions: Set[Tuple[int, int]]) -> None:
        self.name = name
        self.positions = positions
        self.hits = set()

    def __repr__(self):
        return f"Ship('{self.name}', {self.positions})"

    def __str__(self):
        return f"{repr(self)} with hits {self.hits}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ship):
            return NotImplemented
        return self.name == other.name and self.positions == other.positions and self.hits == other.hits

    def _alive_ships_positions(self) -> Set[Tuple[int, int]]:
        """Return the positions of the ship that have not been hit."""
        return self.positions - self.hits

    def is_afloat(self):
        """Return True if the ship has not been sunk."""
        return len(self._alive_ships_positions()) > 0

    def take_shot(self, shot):
        """Check if the shot hits the ship. If so, remember the hit.
        Returns one of 'MISS', 'HIT', or 'DESTROYED'.
        """
        if shot in self._alive_ships_positions():
            self.hits.add(shot)
            if self.is_afloat():
                return "HIT"
            else:
                return "DESTROYED"
        return "MISS"

    @staticmethod
    def _create_ship_from_line(line: str):
        # For example, the line "Carrier 1:1 1:2 1:3 1:4 1:5" encodes a Carrier ship that is placed on the grid at positions (1, 1), (1, 2), (1, 3), (1, 4), and (1, 5).
        entries = line.split()
        name = entries[0]
        positions = {(int(x), int(y)) for x, y in [entry.split(":") for entry in entries[1:]]}
        return Ship(name, positions)


class Grid:
    """Encodes the grid on which the Ships are placed.
    Also remembers the shots fired that missed all of the Ships.
    """

    def __init__(self, x_size: int, y_size: int) -> None:
        self.x_size = x_size
        self.y_size = y_size
        self.ships = []
        self.misses = set()

    def _ship_collides(self, ship: Ship) -> bool:
        """Return True if the ship collides with any other ship on the grid."""
        for other_ship in self.ships:
            if ship.positions.intersection(other_ship.positions):
                return True
        return False

    def add_ship(self, ship: Ship) -> None:
        """
        Add a Ship to the grid at the end of the ships list if it does not
        collide with other ships already there
        """
        if self._ship_collides(ship):
            # not adding a ship because it collides with another ship
            return
        # add this ship to the Grid
        self.ships.append(ship)

    def shoot(self, shot: Tuple[int, int]) -> Tuple[str, Union[Ship, None]]:
        """Shoot at the given position on the grid.
        Returns one of 'MISS', 'HIT', or 'DESTROYED'.
        """
        for ship in self.ships:
            result = ship.take_shot(shot)
            if result == "HIT":
                return "HIT", None
            elif result == "DESTROYED":
                return "DESTROYED", ship
        self.misses.add(shot)
        return "MISS", None

    def random_ship(self) -> Ship:
        """Chooses a type for the ship. Then, randomly chooses a position and orientation for the ship. Returns a Ship object."""
        name, length = random.choice(ship_types)
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            x = random.randint(0, self.x_size - length)
            y = random.randint(0, self.y_size - 1)
            positions = {(x + i, y) for i in range(length)}
        else:
            x = random.randint(0, self.x_size - 1)
            y = random.randint(0, self.y_size - length)
            positions = {(x, y + i) for i in range(length)}
        return Ship(name, positions)

    def create_random(self, n) -> None:
        """Adds random ships to a grid until the desired number of ships is reached:"""
        while len(self.ships) < n:
            ship = self.random_ship()
            self.add_ship(ship)

    @staticmethod
    def _load_grid_from_file(filename: str) -> "Grid":
        """Load a grid from a file."""
        with open(filename) as f:
            lines = f.readlines()
        x_size, y_size = [int(x) for x in lines[0].split(":")]
        grid = Grid(x_size, y_size)
        for line in lines[1:]:
            ship = Ship._create_ship_from_line(line)
            grid.add_ship(ship)
        return grid


def create_ship_from_line(line: str) -> Ship:
    """Create a Ship from a line of text."""
    return Ship._create_ship_from_line(line)


def load_grid_from_file(filename):
    """Load a grid from a file."""
    return Grid._load_grid_from_file(filename)


class BlindGrid:
    """Encodes the opponent's view of the grid."""

    def __init__(self, grid):
        self.grid: Grid = grid
        self.x_size: int = grid.x_size
        self.y_size: int = grid.y_size
        self.misses: Set[Tuple[int, int]] = grid.misses
        self.hits: Set[Tuple[int, int]] = BlindGrid.init_hits(ships=grid.ships)
        self.sunken_ships: List[Ship] = BlindGrid.init_sunken_ships(ships=grid.ships)

    @staticmethod
    def init_hits(ships) -> Set[Tuple[int, int]]:
        """Initialize the hits set."""
        hits = set()
        for ship in ships:
            hits.update(ship.hits)
        return hits

    @staticmethod
    def init_sunken_ships(ships) -> List[Ship]:
        """Initialize the sunken_ships set."""
        sunken_ships = []
        for ship in ships:
            if not ship.is_afloat():
                sunken_ships.append(ship)
        return sunken_ships
