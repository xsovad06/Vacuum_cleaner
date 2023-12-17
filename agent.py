from collections.abc import Callable
from operator import methodcaller
from position import Position
from random import choice
from typing import NamedTuple, List

class Enviroment(NamedTuple):
    """Define the environment for the vacuum cleaner."""

    agent_location: Position
    neighbors: List[Position]
    dirty_locations: List[Position]

class Action:
    """Define Actions for the vacuum cleaner."""

    MOVE_AGENT = "move_agent"
    CLEAN = "clean"
    
    def __init__(self, name, *args, **kwargs):
        self.__name = name
        self.__args = args
        self.__kwargs = kwargs

    def __repr__(self) -> str:
        prams = list(map(str, self.__args)) + list(map(lambda i: f"{i[0]}={i[1]}", self.__kwargs))
        return f"{self.name}{', '.join(prams)}"

    @property
    def name(self):
        return self.__name
    
    def __call__(self, world):
        caller = methodcaller(self.__name, *self.__args, **self.__kwargs)
        return caller(world)

# Define types for readability
History = List[Action]
Memory = []
Agent = Callable[[Enviroment, History, Memory], Action]
Rule = Callable[[Enviroment, History, Memory], Action or None]

# Define rules for the vacuum cleaner
def rule_clean(enviro: Enviroment, history: History, memory: Memory) -> Action or None:
    if enviro.agent_location.dirty:
        return Action(Action.CLEAN, enviro.agent_location)
    return None

def rule_random_move(enviro: Enviroment, history: History, memory: Memory) -> Action or None:
    return Action(Action.MOVE_AGENT, choice(enviro.neighbors))

def rule_move_to_unvisited(enviro: Enviroment, history: History, memory: Memory) -> Action or None:
    for neighbor in enviro.neighbors:
        if neighbor not in memory:
            memory.append(neighbor)
            return Action(Action.MOVE_AGENT, neighbor)
    return None

def rules_agent(rules: List[Rule]) -> Agent:
    """Define the rules-based agent for the vacuum cleaner."""

    def agent(enviro: Enviroment, history: History, memory: Memory) -> Action:
        for rule in rules:
            if action := rule(enviro, history, memory):
                return action
        else:
            print("No rule, agent stops.")
            exit(404)
    return agent

vacuum_agent = rules_agent([
        rule_clean,
        rule_move_to_unvisited,
        rule_random_move
    ])