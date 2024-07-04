from .location import Location
from .constants import *
import random

class State:
    def __init__(self):
        self.gold_location = self._get_gold_location()
        self.wumpus_location = self._get_wumpus_location()
        self.pit_locations = self._get_pit_locations()

        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def initialize(self):
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def _get_gold_location(self):
        x, y = self._get_random_location()
        return Location(x, y)

    def _get_wumpus_location(self):
        x, y = self._get_random_location()
        if Location(x,y) == self.gold_location:
            x,y = self._get_random_location()
        return Location(x, y)

    def _get_random_location(self):
        x = 1
        y = 1

        while (x == 1) and (y == 1):
            x = random.randint(1, WORLD_SIZE)
            y = random.randint(1, WORLD_SIZE)

        return x, y

    def _get_pit_locations(self):
        locations = []
        for x in range(1, WORLD_SIZE + 1):
            for y in range(1, WORLD_SIZE + 1):
                if ((x != 1) or (y != 1)) and (Location(x,y) != self.gold_location or Location(x,y) != self.wumpus_location):
                    if (random.randint(1, 10)) < (PIT_PROBABILITY * 10) + 1:
                        locations.append(Location(x, y))
        return locations
