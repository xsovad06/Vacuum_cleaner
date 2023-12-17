# Simple vacuum cleaner
In the 2D world with obstacles, the rules-based agent is cleaning up.

## Usage
Call the `clean.py` script to do the work. See the program arguments that are required:
- `-s`, `--start`           - Coordinates of starting point (rows, columns).
- `-r`, `--world-heigh`     - Number of rows.
- `-c`, `--world-width`     - Number of columns.
- `-o`, `--obstacles-count` - Number of obstacles to be added to the world randomly.
- `-d`, `--dirt-count`      - Number of dirt to be added to the world randomly.

```bash
python3 simulation.py -s 0 0 -r 6 -c 3 -o 4 -d 6
```

## Example output
For the previous command the following output can by expected. Of course with variations because of the random element placement.
```bash
Starting parameters: start: (0,0), world size: (6, 3)
Generating obstacles: (4)
Generating dirt: (6)
Start simulation
- agent: agent
- world: 
[(0,0)|other|     ]
[**** |     |**** ]
[**** |     |other]
[     |**** |     ]
[     |chair|table]
[**** |     |     ]

0: Dirty locations: 5 -> Action: move_agent(1,0)
1: Dirty locations: 5 -> Action: clean(1,0)
2: Dirty locations: 4 -> Action: move_agent(0,0)
3: Dirty locations: 4 -> Action: move_agent(1,1)
4: Dirty locations: 4 -> Action: move_agent(1,2)
5: Dirty locations: 4 -> Action: clean(1,2)
6: Dirty locations: 3 -> Action: move_agent(0,2)
7: Dirty locations: 3 -> Action: move_agent(1,2)
8: Dirty locations: 3 -> Action: move_agent(2,1)
9: Dirty locations: 3 -> Action: move_agent(3,1)
10: Dirty locations: 3 -> Action: clean(3,1)
11: Dirty locations: 2 -> Action: move_agent(3,2)
12: Dirty locations: 2 -> Action: move_agent(2,1)
13: Dirty locations: 2 -> Action: move_agent(2,0)
14: Dirty locations: 2 -> Action: clean(2,0)
15: Dirty locations: 1 -> Action: move_agent(3,0)
16: Dirty locations: 1 -> Action: move_agent(4,0)
17: Dirty locations: 1 -> Action: move_agent(5,0)
18: Dirty locations: 1 -> Action: clean(5,0)
19: Agent cleaned all locations

[-----|other|-----]
[-----|-----|-----]
[-----|-----|other]
[-----|-----|-----]
[-----|chair|table]
[-----|     |     ]

CacheInfo(hits=21, misses=13, maxsize=9223372036854775807, currsize=13)
```