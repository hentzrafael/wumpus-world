import random
from .perception import Perception
from .constants import *

class Agent(object):
    @staticmethod
    def process(percept: Perception):
        return_list = []
        if percept.stench == 1:
            return_list.append(random.choice([TURNLEFT, TURNRIGHT, SHOOT, GOFORWARD]))
        if percept.breeze == 1:
            return_list.append(random.choice([TURNLEFT, TURNRIGHT,GOFORWARD]))
        if percept.glitter == 1:
            return_list.append(GRAB)
            return_list.append(GOFORWARD)
        if percept.bump == 1:
            return_list.append(random.choice([TURNLEFT, TURNRIGHT,GOFORWARD]))
        else:
            return_list.append(GOFORWARD)

        return return_list
