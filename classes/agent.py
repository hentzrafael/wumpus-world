import random
from .perception import Perception
from .constants import *

class Agent(object):
    @staticmethod
    def process(percept: Perception):
        return_list = []
        if percept.stench == 1:
            return_list.append(random.choice([TURNLEFT, TURNRIGHT, SHOOT]))
        if percept.breeze == 1:
            return_list.append(random.choice([TURNLEFT, TURNRIGHT]))
        if percept.glitter == 1:
            return_list.append(GRAB)
        if percept.bump == 1:
            return_list.append(random.choice([TURNLEFT, TURNRIGHT]))

        return_list.append(GOFORWARD)
        return return_list
