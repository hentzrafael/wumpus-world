import random
import pygame

from .well import Well
from .agent import Agent
from .wumpus import Wumpus
from .gold import Gold


GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 50

SCREEN_WIDTH = GRID_SIZE * CELL_SIZE + 2 * MARGIN
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + 2 * MARGIN + 50 

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
class App():
    DESCONHECIDO = 0
    WUMPUS = 1
    WELL = 2
    GOLD = 3
    SEGURO = 4
    CHEIRO = 5
    BRISA = 6
    
    rows = 4
    cols = 4
    score = 0

    grid = {
        (0,0): [],
        (0,1): [],
        (0,2): [],
        (0,3): [],
        (1,0): [],
        (1,1): [],
        (1,2): [],
        (1,3): [],
        (2,0): [],
        (2,1): [],
        (2,2): [],
        (2,3): [],
        (3,0): [],
        (3,1): [],
        (3,2): [],
        (3,3): [],
    }

    def __init__(self) -> None:
        self.__place_wells()
        self.place_agent()
        self.place_wumpus()
        self.place_gold()
        self.place_cheiro()
        self.place_brisa()
        print(self.grid)
        
    def __place_wells(self):
        for row, col in self.grid.keys():
            if row == 0 and col == 0:
                continue
            chance = random.randint(1,10)
            if chance < 3:
                self.grid[(row, col)].append(Well())

    def place_agent(self):
        self.grid[(0, 0)].append(Agent())

    def place_wumpus(self):
        random_x = random.randint(0,3)
        random_y = random.randint(0,3)
        if self.contains_type(self.grid[(random_x,random_y)], Agent) or self.contains_type(self.grid[(random_x,random_y)], Well):
            self.place_wumpus()
            return
        self.grid[(random_x, random_y)].append(Wumpus())


    def place_gold(self):
        random_x = random.randint(0,3)
        random_y = random.randint(0,3)
        if self.contains_type(self.grid[(random_x,random_y)], Agent) or self.contains_type(self.grid[(random_x,random_y)], Well) or self.contains_type(self.grid[(random_x,random_y)], Wumpus):
            self.place_gold()
            return
        self.grid[(random_x, random_y)].append(Gold())

    def place_cheiro(self):
        for key, value in self.grid.items():
            if self.contains_type(value, Wumpus):
                position = key
        
        # Cria o array de adjacentes
        cheiros_position = [(position[0] - 1, position[1]),(position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]
        cheiros_position = [tupla for tupla in cheiros_position if 0 <= tupla[0] <= 3 and 0 <= tupla[1] <= 3]
        for cheiro in cheiros_position:
            self.grid[cheiro].append(self.CHEIRO)
        


    def place_brisa(self):
        well_positions = []
        for key, value in self.grid.items():
            if self.contains_type(value, Well):
                well_positions.append(key)
        print("Wells: ")
        print(well_positions)
        for position in well_positions:
            # Cria o array de adjacentes
            brisa_position = [(position[0] - 1, position[1]),(position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]
            brisa_position = [tupla for tupla in brisa_position if 0 <= tupla[0] <= 3 and 0 <= tupla[1] <= 3]
            
            for brisa in brisa_position:
                self.grid[brisa].append(self.BRISA)
        

    
    def contains_type(self,lst, typ):
        return any(isinstance(item, typ) for item in lst)

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * CELL_SIZE + MARGIN
                y = row * CELL_SIZE + MARGIN
                color = WHITE
                if self.contains_type(self.grid[(row,col)], Well):
                    color = BLACK
                elif self.contains_type(self.grid[(row,col)], Wumpus):
                    color = RED
                elif self.contains_type(self.grid[(row,col)], Gold):
                    color = YELLOW
                elif self.contains_type(self.grid[(row,col)], Agent):
                    color = GREEN
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, BLACK)
        screen.blit(score_text, (MARGIN, SCREEN_HEIGHT - 50))
