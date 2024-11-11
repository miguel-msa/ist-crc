import numpy as np
from typing import Literal, Dict, List
from dataclasses import dataclass
import math
from common import RANDOM_SEEDED, SIMULATION_PARAMS

class Agent:
    def __init__(self, id: int, p: int, q: int):
        self.id = id
        self.p = p
        self.q = q
        self.fitness = 0
        self.last_play_by_neighbor: Dict[int, NeighborPlay] = {}
        self.playing_round = 0
        self.play_flag = 0
        self.cooperate_flag = 0
        self.defect_flag = 0

    def play_with_neighbors(self, neighbors_to_play: List['Agent']):
        self.playing_round += 1

        # filter out neighbors that have already played with this agent
        neighbors_left_to_play = list(filter(lambda n: self.playing_round > n.playing_round, neighbors_to_play))

        for idx, _ in enumerate(neighbors_left_to_play):
            neighbor_agent: Agent = neighbors_left_to_play[idx]
            x_choice = self.play(neighbor_agent)
            y_choice = neighbor_agent.play(self)


            self.store_neighbor_choice(neighbor_agent.id, y_choice)
            neighbor_agent.store_neighbor_choice(self.id, x_choice)

            from utils import distribute_payoff
            self_payoff, neighbor_payoff = distribute_payoff(x_choice, y_choice)
            self.fitness += self_payoff
            neighbor_agent.fitness += neighbor_payoff



    def play(self, neighbor: 'Agent') -> Literal['C', 'D']:

        if self.playing_round == 1:
            first_response = self.first_response()

            return first_response
            # get the last choice the neighbord made when playing with this agent
        last_neighbor_choice = self.last_play_by_neighbor[neighbor.id]

        if last_neighbor_choice is None:
            first_response = self.first_response()
            if(first_response == 'C'):
                self.play_flag += 1
                self.cooperate_flag += 1
            elif(first_response == 'D'):
                self.play_flag += 1
                self.defect_flag += 1

            return first_response

        if last_neighbor_choice == 'C':
            if(RANDOM_SEEDED.random() < self.p):
                self.play_flag += 1
                self.cooperate_flag += 1
                return 'C'
            else:
                self.play_flag += 1
                self.defect_flag += 1
                return 'D'
        elif last_neighbor_choice == 'D':
            if (RANDOM_SEEDED.random() < self.q):
                self.play_flag += 1
                self.cooperate_flag += 1
                return 'C'
            else:
                self.play_flag += 1
                self.defect_flag += 1
                return 'D'


    def first_response(self) -> Literal['C', 'D']:
        return 'C' if RANDOM_SEEDED.random() < (self.p + self.q)/2 else 'D'

    def store_neighbor_choice(self, neighbor_id: int, choice: Literal['C', 'D']) -> None:
        self.last_play_by_neighbor[neighbor_id] = choice

    '''
    on each simulation time step, 2 neighbors are randomly picked (x and y) and calculate their individual payoff (fitness)
    player x adopts the strategy of player y with a probability given by the function adopt_strategy
    '''
    def adopt_strategy(self, fitness_y, p_y, q_y):
        adoption_probability = 1/(1 + np.exp((self.fitness - fitness_y)/SIMULATION_PARAMS['K']))

        if RANDOM_SEEDED.random() < adoption_probability:
            xi_1 = RANDOM_SEEDED.normal(0, SIMULATION_PARAMS['SIGMA'])
            xi_2 = RANDOM_SEEDED.normal(0, SIMULATION_PARAMS['SIGMA'])

            self.p = p_y + xi_1
            if(self.p > 1):
                self.p = 1
            elif(self.p < 0):
                self.p = 0

            self.q = q_y + xi_2
            if(self.q > 1):
                self.q = 1
            elif(self.q < 0):
                self.q = 0

    def __str__(self):
        return f"Agent({self})"


@dataclass
class NeighborPlay:
    sim_step: int
    choice: Literal['C', 'D']
