import pygame
from classes.world import World
from classes.agent import Agent
from classes.constants import *

MAX_MOVES_PER_GAME = 1000

WORLD_SIZE = 4

CELL_SIZE = 100
MARGIN = 50
SCREEN_WIDTH = WORLD_SIZE * CELL_SIZE + 2 * MARGIN + 100
SCREEN_HEIGHT = WORLD_SIZE * CELL_SIZE + 2 * MARGIN + 50 

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mundo do Wumpus")

    clock = pygame.time.Clock()
    world = World() 

    num_moves = 0
    running = True
    win = False
    while running:
        
        while (not world.game_over()) and (num_moves < MAX_MOVES_PER_GAME):
            screen.fill(WHITE)
            world.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            percept = world.get_percept()  
            actions = Agent.process(percept)

            for action in actions:
                if action == SHOOT and not world.current_state.agent_has_arrow:
                    continue
                if action == GRAB:
                    world.execute_action(action)
                    win = True
                    break
                world.execute_action(action)
                num_moves += 1

            if win:
                break

            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f'Score: {world.get_score()}', True, BLACK)
            actions_string = [action_to_string(x) for x in actions]
            actions_text = font.render(f'Ações: {",".join(actions_string)}', True, BLACK)
            screen.blit(score_text, ((SCREEN_WIDTH // 2) - (score_text.get_width() // 2), 20))
            screen.blit(actions_text, ((SCREEN_WIDTH // 2) - (actions_text.get_width() // 2), 40))
            pygame.display.flip()
            clock.tick(1)

        if world.game_over() and not win:
            screen.fill(WHITE)
            game_over_text = font.render(f'GAME OVER', True, BLACK)
            screen.blit(game_over_text, ((SCREEN_WIDTH // 2) - (score_text.get_width() // 2), (SCREEN_HEIGHT // 2) - (game_over_text.get_height() // 2)))
            pygame.display.flip()
        if win:
            screen.fill(WHITE)
            win_text = font.render(f'Vitória!', True, BLACK)
            screen.blit(win_text, ((SCREEN_WIDTH // 2) - (score_text.get_width() // 2), (SCREEN_HEIGHT // 2) - (win_text.get_height() // 2)))
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()




def action_to_string(action):
    """ action_to_string: return a string from the given action """
    if action == GOFORWARD:
        return "GOFORWARD"
    if action == TURNRIGHT:
        return "TURNRIGHT"
    if action == TURNLEFT:
        return "TURNLEFT"
    if action == SHOOT:
        return "SHOOT"
    if action == GRAB:
        return "GRAB"
    return "UNKNOWN ACTION"


main()
