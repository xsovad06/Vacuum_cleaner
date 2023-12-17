import argparse
from agent import Agent, Enviroment, vacuum_agent
from position import Position, Obstacle, Dirt, obstacle_names, generate_random_objects_placement
from world import World

def parse_arguments():
    """Argument parser."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', nargs='+', type=int, required=True,help='Coordinates of starting point (rows, columns).')
    parser.add_argument('-r', '--world-heigh', type=int, required=True, help='Number of rows.')
    parser.add_argument('-c', '--world-width', type=int, required=True, help='Number of columns.')
    parser.add_argument('-o', '--obstacles-count', type=int, required=True, help='Number of obstacles to be added to the map randomly.')
    parser.add_argument('-d', '--dirt-count', type=int, required=True, help='Number of dirt to be added to the map randomly.')
    return parser.parse_args()

def simulation_loop(agent: Agent, world: World) -> None:
    """Simulation loop for running the agent."""

    print(f"Start simulation")
    print(f"- agent: {agent.__name__}")
    print(f"- world: {world}")

    counter = 0
    history = []
    memory = []

    while world.dirty_locations:
        enviro = Enviroment(
            world.agent_location,
            world.get_neighbors(),
            world.dirty_locations,
        )
        print(f"{counter}: Dirty locations: {len(world.dirty_locations)}", end=" -> ")
        action = agent(enviro, history, memory)

        history.append(action)
        print(f"Action: {action}")
        action(world)

        counter += 1

    else:
        print(f"{counter}: Agent cleaned all locations")


if __name__ == "__main__":
    args = parse_arguments()
    start = Position(args.start[0], args.start[1])

    rows = args.world_heigh
    columns = args.world_width
    world = World(rows, columns, start)
    print(f'Starting parameters: start: {start}, world size: ({rows}, {columns})')

    obstacles = generate_random_objects_placement(args.obstacles_count, rows, columns, Obstacle, obstacle_names, [start.get_coordinates_tuple()])
    print(f'Generating obstacles: ({len(obstacles)})')
    world.add_obstacles(obstacles)

    dirt_list = generate_random_objects_placement(args.dirt_count, rows, columns, Dirt, exclude_points = [start.get_coordinates_tuple()] + [o.get_coordinates_tuple() for o in obstacles])
    print(f'Generating dirt: ({len(dirt_list)})')
    world.add_dirt(dirt_list)

    simulation_loop(vacuum_agent, world)
    world.print_map()
    print(Position.__new__.cache_info())