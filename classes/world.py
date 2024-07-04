from .state import State
from .perception import Perception
from .location import Location
from .constants import *
import pygame

class World:
    score = 0
    world_size = WORLD_SIZE
    def __init__(self):
        self.num_actions = 0

        self.current_state = State()
        self.current_percept = Perception()

        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
           (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

        

    def initialize(self):
        self.num_actions = 0
        self.current_state.initialize()
        self.current_percept.initialize()

        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
           (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True

        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True

        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def get_percept(self):
        return self.current_percept

    def execute_action(self, action):
        self.num_actions += 1
        self.current_percept.bump = False
        self.current_percept.scream = False

        if action == GOFORWARD:
            if self.current_state.agent_orientation == RIGHT:
                if self.current_state.agent_location.x < WORLD_SIZE:
                    self.current_state.agent_location.x += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == UP:
                if self.current_state.agent_location.y < WORLD_SIZE:
                    self.current_state.agent_location.y += 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == LEFT:
                if self.current_state.agent_location.x > 1:
                    self.current_state.agent_location.x -= 1
                else:
                    self.current_percept.bump = True
            elif self.current_state.agent_orientation == DOWN:
                if self.current_state.agent_location.y > 1:
                    self.current_state.agent_location.y -= 1
                else:
                    self.current_percept.bump = True

            self.current_percept.glitter = False

            if (not self.current_state.agent_has_gold) and \
                    (self.current_state.agent_location == self.current_state.gold_location):
                self.current_percept.glitter = True

            self.current_percept.stench = False

            if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
                    (self.current_state.agent_location == self.current_state.wumpus_location):
                self.current_percept.stench = True

            self.current_percept.breeze = False

            for pit in self.current_state.pit_locations:
                if Location.adjacent(self.current_state.agent_location, pit):
                    self.current_percept.breeze = True
                elif self.current_state.agent_location == pit:
                    self.current_state.agent_alive = False

            if self.current_state.wumpus_alive and \
                    (self.current_state.agent_location == self.current_state.wumpus_location):
                self.current_state.agent_alive = False

        if action == TURNLEFT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = LEFT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = RIGHT

        if action == TURNRIGHT:
            if self.current_state.agent_orientation == RIGHT:
                self.current_state.agent_orientation = DOWN
            elif self.current_state.agent_orientation == UP:
                self.current_state.agent_orientation = RIGHT
            elif self.current_state.agent_orientation == LEFT:
                self.current_state.agent_orientation = UP
            elif self.current_state.agent_orientation == DOWN:
                self.current_state.agent_orientation = LEFT

        if action == GRAB:
            if not self.current_state.agent_has_gold and \
                    (self.current_state.agent_location == self.current_state.gold_location):
                self.current_state.agent_has_gold = True
                self.current_percept.glitter = False

        if action == SHOOT:
            if self.current_state.agent_has_arrow:
                self.current_state.agent_has_arrow = False

                if self.current_state.wumpus_alive:
                    if (((self.current_state.agent_orientation == RIGHT) and
                         (self.current_state.agent_location.x < self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y == self.current_state.wumpus_location.y)) or
                        ((self.current_state.agent_orientation == UP) and
                         (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y < self.current_state.wumpus_location.y)) or
                        ((self.current_state.agent_orientation == LEFT) and
                         (self.current_state.agent_location.x > self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y == self.current_state.wumpus_location.y)) or
                        ((self.current_state.agent_orientation == DOWN) and
                         (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and
                         (self.current_state.agent_location.y > self.current_state.wumpus_location.y))):
                        self.current_state.wumpus_alive = False
                        self.current_percept.scream = True

    def game_over(self):
        return not self.current_state.agent_alive

    def get_score(self):
        score = 0

        score -= self.num_actions

        if not self.current_state.agent_has_arrow:
            score -= 9

        if self.current_state.agent_has_gold:
            score += 1000

        if not self.current_state.agent_alive:
            score -= 1000

        return score

    def draw(self, screen):
        for row in range(WORLD_SIZE, 0, -1):
            for col in range(WORLD_SIZE,0, -1 ):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                color = WHITE
                if Location(row,col) in self.current_state.pit_locations:
                    color = BLACK
                elif Location(row,col) ==  self.current_state.wumpus_location:
                    color = RED
                elif Location(row,col) == self.current_state.agent_location:
                    color = GREEN   
                elif Location(row,col) == self.current_state.gold_location and self.current_state.agent_has_gold:
                    color = WHITE
                elif Location(row,col) == self.current_state.gold_location:
                    color = YELLOW
                
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
