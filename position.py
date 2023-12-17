import random
from functools import lru_cache
from sys import maxsize
from typing import NamedTuple, Union, List, Tuple

obstacle_names = ['table', 'chair', 'bed', 'other']

class Dirt(NamedTuple):
    row: int
    column: int

    def __repr__(self) -> str:
        return f"({self.row},{self.column})"

    def __str__(self) -> str:
        return self.__repr__()

class Obstacle(NamedTuple):
    row: int
    column: int
    name: str

    def __str__(self) -> str:
        return self.name

    def get_coordinates_tuple(self) -> Tuple[int]:
        return (self.row, self.column)

def generate_random_objects_placement(
    object_count: int,
    max_row: int,
    max_column: int,
    object_class: Union[type(Obstacle), type(Dirt)],
    object_names: List[str] = None,
    exclude_points: List[Tuple[int]] = None) -> List[Obstacle]:
    """Generate list of random obstacles with random positions on the map."""

    objects = []
    i = 0
    while i < object_count:
        row = random.randint(0, max_row - 1)
        column = random.randint(0, max_column - 1)

        if exclude_points and (row, column) in exclude_points:
            continue

        if object_class == Obstacle:
            name_idx = random.randint(0, len(object_names) - 1)
            objects.append(Obstacle(row, column, object_names[name_idx]))
        elif object_class == Dirt:
            objects.append(Dirt(row, column))

        i += 1

    return objects

class Position:
    @lru_cache(maxsize=maxsize)
    def __new__(cls, row: int, column: int, dirty: bool = False) -> 'Position':
        instance = super().__new__(cls)
        instance.__row = row
        instance.__column = column
        instance.__dirty = dirty
        return instance

    def __hash__(self) -> int:
        return hash((self.__row, self.__column))
    
    def __repr__(self) -> str:
        return f"({self.__row},{self.__column})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column

    @property
    def dirty(self) -> bool:
        return self.__dirty
    
    @dirty.setter
    def dirty(self, dirty):
        self.__dirty = dirty
    
    def get_coordinates_tuple(self) -> Tuple[int]:
        return (self.__row, self.__column)