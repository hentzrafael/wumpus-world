import pygame
import random
from classes.app import App
from classes.well import Well
from classes.gold import Gold
from classes.wumpus import Wumpus
from classes.agent import Agent


# Dimensões da tela e do labirinto
GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 50
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE + 2 * MARGIN
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + 2 * MARGIN + 50  # Espaço adicional para a pontuação

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Definindo as entidades do jogo
EMPTY = 0
PIT = 1
WUMPUS = 2
GOLD = 3
AGENT = 4

class WumpusWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = App().grid
        self.agent_position = (0, 0)
        self.agent_has_gold = False
        self.agent_has_arrow = True
        self.wumpus_alive = True
        self.score = 0
        # self.place_entities()
    
    def place_entities(self):
        # Colocando o agente na posição inicial
        self.grid[0][0] = AGENT
        
        # Colocando poços, Wumpus e ouro aleatoriamente
        self.place_random_entity(PIT, 3)  # Menos poços em um labirinto menor
        self.place_random_entity(WUMPUS, 1)
        self.place_random_entity(GOLD, 1)
        
    def place_random_entity(self, entity, count):
        placed = 0
        while placed < count:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = entity
                placed += 1
                
    def move_agent(self, direction):
        row, col = self.agent_position
        if direction == 'UP' and row > 0:
            self.grid[row][col] = EMPTY
            self.agent_position = (row - 1, col)
        elif direction == 'DOWN' and row < self.rows - 1:
            self.grid[row][col] = EMPTY
            self.agent_position = (row + 1, col)
        elif direction == 'LEFT' and col > 0:
            self.grid[row][col] = EMPTY
            self.agent_position = (row, col - 1)
        elif direction == 'RIGHT' and col < self.cols - 1:
            self.grid[row][col] = EMPTY
            self.agent_position = (row, col + 1)
        
        row, col = self.agent_position
        self.score -= 1  # Cada movimento custa 1 ponto
        if self.grid[row][col] == GOLD:
            self.agent_has_gold = True
            self.score += 1000
            print("Você encontrou o ouro!")
        elif self.grid[row][col] == PIT:
            self.score -= 1000
            print("Você caiu em um poço! Você perdeu!")
        elif self.grid[row][col] == WUMPUS and self.wumpus_alive:
            self.score -= 1000
            print("O Wumpus te pegou! Você perdeu!")
        self.grid[row][col] = AGENT

        if self.agent_has_gold and not self.wumpus_alive:
            print("Você venceu! Pegou o ouro e matou o Wumpus!")
    
    def shoot_arrow(self, direction):
        if not self.agent_has_arrow:
            return
        self.agent_has_arrow = False
        self.score -= 10
        row, col = self.agent_position
        if direction == 'UP':
            for r in range(row-1, -1, -1):
                if self.grid[r][col] == WUMPUS:
                    self.grid[r][col] = EMPTY
                    self.wumpus_alive = False
                    print("Você matou o Wumpus!")
                    break
                elif self.grid[r][col] == PIT:
                    continue  # Flecha pode atravessar poços
        elif direction == 'DOWN':
            for r in range(row+1, self.rows):
                if self.grid[r][col] == WUMPUS:
                    self.grid[r][col] = EMPTY
                    self.wumpus_alive = False
                    print("Você matou o Wumpus!")
                    break
                elif self.grid[r][col] == PIT:
                    continue
        elif direction == 'LEFT':
            for c in range(col-1, -1, -1):
                if self.grid[row][c] == WUMPUS:
                    self.grid[row][c] = EMPTY
                    self.wumpus_alive = False
                    print("Você matou o Wumpus!")
                    break
                elif self.grid[row][c] == PIT:
                    continue
        elif direction == 'RIGHT':
            for c in range(col+1, self.cols):
                if self.grid[row][c] == WUMPUS:
                    self.grid[row][c] = EMPTY
                    self.wumpus_alive = False
                    print("Você matou o Wumpus!")
                    break
                elif self.grid[row][c] == PIT:
                    continue

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * CELL_SIZE + MARGIN
                y = row * CELL_SIZE + MARGIN
                color = WHITE
                if type(self.grid[row][col]) == Well:
                    color = BLACK
                elif type(self.grid[row][col]) == Wumpus:
                    color = RED
                elif type(self.grid[row][col]) == Gold:
                    color = YELLOW
                elif type(self.grid[row][col]) == Agent:
                    color = GREEN
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, BLACK)
        screen.blit(score_text, (MARGIN, SCREEN_HEIGHT - 50))

class IntelligentAgent:
    def __init__(self, world):
        self.world = world
        self.path = []
        self.find_path()
        
    def find_path(self):
        # Implementação simples de uma busca em largura para encontrar o caminho até o ouro
        from collections import deque
        start = self.world.agent_position
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            if self.world.grid[current[0]][current[1]] == GOLD:
                self.reconstruct_path(current, parent)
                return
            
            for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                row, col = current
                if direction == 'UP':
                    next_pos = (row - 1, col)
                elif direction == 'DOWN':
                    next_pos = (row + 1, col)
                elif direction == 'LEFT':
                    next_pos = (row, col - 1)
                elif direction == 'RIGHT':
                    next_pos = (row, col + 1)
                
                if 0 <= next_pos[0] < self.world.rows and 0 <= next_pos[1] < self.world.cols:
                    if next_pos not in visited and self.world.grid[next_pos[0]][next_pos[1]] != PIT:
                        queue.append(next_pos)
                        visited.add(next_pos)
                        parent[next_pos] = current
                        
    def reconstruct_path(self, end, parent):
        self.path = []
        while end is not None:
            self.path.append(end)
            end = parent[end]
        self.path.reverse()
        
    def next_move(self):
        row, col = self.world.agent_position
        # Verifica se o Wumpus está na mesma linha ou coluna e atira a flecha
        for r in range(self.world.rows):
            if self.world.grid[r][col] == WUMPUS:
                self.world.shoot_arrow('UP' if r < row else 'DOWN')
                return None  # Não se move após atirar
        for c in range(self.world.cols):
            if self.world.grid[row][c] == WUMPUS:
                self.world.shoot_arrow('LEFT' if c < col else 'RIGHT')
                return None  # Não se move após atirar
        
        if self.path:
            next_pos = self.path.pop(0)
            if next_pos == (row - 1, col):
                return 'UP'
            elif next_pos == (row + 1, col):
                return 'DOWN'
            elif next_pos == (row, col - 1):
                return 'LEFT'
            elif next_pos == (row, col + 1):
                return 'RIGHT'
        return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mundo do Wumpus")

    clock = pygame.time.Clock()
    world = App()
    agent = Agent()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        move = agent.can_move(world.grid)
        if move:    
            agent.move(move)
        
        screen.fill(WHITE)
        world.draw(screen)
        pygame.display.flip()
        clock.tick(1)
    
    pygame.quit()

if __name__ == "__main__":
    main()
