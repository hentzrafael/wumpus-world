from .well import Well
from .wumpus import Wumpus
from .gold import Gold

class Agent():
    DESCONHECIDO = 0
    WUMPUS = 1
    WELL = 2
    GOLD = 3
    SEGURO = 4
    CHEIRO = 5
    BRISA = 6

    score = 0

    x = 0
    y = 0

    conhecimento = {
        (0,0): [SEGURO],
        (0,1): [DESCONHECIDO],
        (0,2): [DESCONHECIDO],
        (0,3): [DESCONHECIDO],
        (1,0): [DESCONHECIDO],
        (1,1): [DESCONHECIDO],
        (1,2): [DESCONHECIDO],
        (1,3): [DESCONHECIDO],
        (2,0): [DESCONHECIDO],
        (2,1): [DESCONHECIDO],
        (2,2): [DESCONHECIDO],
        (2,3): [DESCONHECIDO],
        (3,0): [DESCONHECIDO],
        (3,1): [DESCONHECIDO],
        (3,2): [DESCONHECIDO],
        (3,3): [DESCONHECIDO],
    }

    def move(self):
        pass


    def contains_type(self,lst, typ):
        return any(isinstance(item, typ) for item in lst)


    def can_move(self, app_grid) -> bool:
        self.check_actual_position((self.x, self.y),app_grid)

    def check_actual_position(self, position: tuple, app_grid: dict):
        # Atualiza o conhecimento
        self.conhecimento[position].append(app_grid[position])

        if self.contains_type(app_grid[position], Well) or self.contains_type(app_grid[position], Wumpus):
            self.score -= 1000
        elif self.contains_type(app_grid[position], Gold):
            self.score += 1000

        self.score -= 1


        # Cria o array de movimentos possíveis
        possible_movements = [(position[0] - 1, position[1]),(position[0] + 1, position[1]), (position[0], position[1] - 1), (position[0], position[1] + 1)]
        for index,tupla in enumerate(possible_movements):
            if (tupla[0] < 0 or tupla[0] > 3) or (tupla[1] < 0 or tupla[1] > 3):
                possible_movements.pop(index)
        
        # Checar se tem cheiro nas proximidades
        pontuacao = {}
        for movimento in possible_movements:
            pontuacao[movimento] = 0
            if self.conhecimento[movimento].count(self.CHEIRO) > 0:
                pontuacao[movimento] -= 1
            
            if self.conhecimento[movimento].count(self.BRISA) > 0:
                pontuacao[movimento] -= 1
            
            if self.conhecimento[movimento].count(self.SEGURO) > 0:
                pontuacao[movimento] += 1

        sorted_items = sorted(pontuacao.items(), key=lambda item: item[1])

        sorted_list = list(sorted_items)

        self.x = sorted_list[0][0][0]
        self.y = sorted_list[0][0][1]

        print(position)
        
        app_grid[(self.x,self.y)].append(Agent())
        app_grid[position] = [x for x in app_grid[position] if isinstance(x, Agent)]

        
        
    def __repr__(self) -> str:
        return "Agent"