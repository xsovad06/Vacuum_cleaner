from typing import List, Tuple, Union
from position import Position, Obstacle, Dirt

class World:
    """Define the world for the vacuum cleaner."""

    def __init__(self, row_count: int, column_count: int, agent: Position) -> None:
        self.__map_rows = row_count
        self.__map_columns = column_count
        self.__map = []
        self.__agent_location = agent
        self.__dirty_locations = []

        for _ in range(row_count):
            row = [None] * column_count
            self.__map.append(row)

        self.__map[agent.row][agent.column] = agent

    def __str__(self) -> str:
        result = "\n"
        for r in range(self.__map_rows):
            items = [f"{str('****' if isinstance(value, Position) and value.dirty else value):<{5}}" if value is not None else "     " for value in self.__map[r]]
            result += "[" + "|".join(items) + "]\n"
        return result
    
    @property
    def agent_location(self) -> Position:
        return self.__agent_location

    @property
    def dirty_locations(self) -> List[Tuple[int]]:
        return self.__dirty_locations

    def print_map(self) -> None:
        result = "\n"
        for r in range(self.__map_rows):
            items = []
            for value in self.__map[r]:
                if value is not None:
                    if isinstance(value, Position) and value.dirty:
                        item = "*****"
                    elif isinstance(value, Position):
                        item = "-----"
                    else:
                        item = value
                    items.append(f"{str(item):<{5}}")
                else:
                    items.append("     ")
            result += "[" + "|".join(items) + "]\n"
        print(result)

    def check_if_in_map_range(self, position: Union[Position, Obstacle]) -> bool:
        return 0 <= position.row < self.__map_rows and 0 <= position.column < self.__map_columns

    def add_obstacles(self, obstacles: List[Obstacle]) -> None:
        for obstacle in obstacles:
            if self.check_if_in_map_range(obstacle) and not isinstance(self.__map[obstacle.row][obstacle.column], Obstacle):
                self.__map[obstacle.row][obstacle.column] = obstacle

    def add_dirt(self, dirt_list: List[Dirt]) -> None:
        for dirt in dirt_list:
            dirt_location = Position(dirt.row, dirt.column, dirty=True)
            dirt_tuple = dirt_location.get_coordinates_tuple()
            if self.check_if_in_map_range(dirt) and dirt_tuple not in self.__dirty_locations:
                if isinstance(self.__map[dirt.row][dirt.column], Position):
                    self.__map[dirt.row][dirt.column].dirt = True
                else:
                    self.__map[dirt.row][dirt.column] = dirt_location

                self.__dirty_locations.append(dirt_tuple)

    def get_neighbors(self) -> List[Position]:
        neighbors = []
        row, column = self.agent_location.row, self.agent_location.column

        # Cartesian neighbors
        if row > 0:                                                     # north neighbor
            next_row = row - 1
            if not isinstance(self.__map[next_row][column], Obstacle):
                neighbors.append(self.__map[next_row][column]) if isinstance(self.__map[next_row][column], Position) else neighbors.append(Position(next_row, column))
        if column < self.__map_columns - 1:                             # east neighbor
            next_column = column + 1
            if not isinstance(self.__map[row][next_column], Obstacle):
                neighbors.append(self.__map[row][next_column]) if isinstance(self.__map[row][next_column], Position) else neighbors.append(Position(row, next_column))
        if row < self.__map_rows - 1:                                   # south neighbor
            next_row = row + 1
            if not isinstance(self.__map[next_row][column], Obstacle):
                neighbors.append(self.__map[next_row][column]) if isinstance(self.__map[next_row][column], Position) else neighbors.append(Position(next_row, column))
        if column > 0:                                                  # west neighbor
            next_column = column - 1
            if not isinstance(self.__map[row][next_column], Obstacle):
                neighbors.append(self.__map[row][next_column]) if isinstance(self.__map[row][next_column], Position) else neighbors.append(Position(row, next_column))

        # Diagonal neighbors
        if row > 0 and column < self.__map_columns - 1:                   # northeast neighbor
            next_row = row - 1
            next_column = column + 1
            if not isinstance(self.__map[next_row][next_column], Obstacle):
                neighbors.append(self.__map[next_row][next_column]) if isinstance(self.__map[next_row][next_column], Position) else neighbors.append(Position(next_row, next_column))
        if row < self.__map_rows - 1 and column < self.__map_columns - 1: # southeast neighbor
            next_row = row + 1
            next_column = column + 1
            if not isinstance(self.__map[next_row][next_column], Obstacle):
                neighbors.append(self.__map[next_row][next_column]) if isinstance(self.__map[next_row][next_column], Position) else neighbors.append(Position(next_row, next_column))
        if row < self.__map_rows - 1 and column > 0:                      # soutwest neighbor
            next_row = row + 1
            next_column = column - 1
            if not isinstance(self.__map[next_row][next_column], Obstacle):
                neighbors.append(self.__map[next_row][next_column]) if isinstance(self.__map[next_row][next_column], Position) else neighbors.append(Position(next_row, next_column))
        if row > 0 and column > 0:                                        # norhtwest neighbor
            next_row = row - 1
            next_column = column - 1
            if not isinstance(self.__map[next_row][next_column], Obstacle):
                neighbors.append(self.__map[next_row][next_column]) if isinstance(self.__map[next_row][next_column], Position) else neighbors.append(Position(next_row, next_column))

        return neighbors

    def clean(self, location: Position):
        if location.dirty:
            location.dirty = False
            for dirty_location in self.dirty_locations:
                if dirty_location[0] == location.row and dirty_location[1] == location.column:
                    self.dirty_locations.remove(dirty_location)

    def move_agent(self, location: Position):
        assert self.check_if_in_map_range(location), f'Can not move to {location}, not in the world map!'
        # add the position object to the map
        self.__map[location.row][location.column] = location
        self.__agent_location = location
