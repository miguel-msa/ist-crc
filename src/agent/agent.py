from typing import Literal, Dict, List
from dataclasses import dataclass
import math
from common import RANDOM_SEEDED, SIMULATION_PARAMS, distribute_payoff

class Agent:
    def __init__(self, id: int, p: int, q: int):
        self.id = id
        self.p = p
        self.q = q
        self.fitness = 0 # todo: increase on every game
        self.last_play_by_neighbor: Dict[int, NeighborPlay] = {}
        self.playing_round = 0

    # neighbors = {
    #     2: [],
    #     5: [True, True],
    # }

    def play_with_neighbors(self, neighbors_left_to_play: List['Agent']):
        self.playing_round += 1
        # filter out neighbors that have already played with this agent
        neighbors_left_to_play = list(filter(lambda n: self.playing_round > n.playing_round, neighbors_left_to_play))
        for neighbor in neighbors_left_to_play:
            neighbor_agent: Agent = neighbors_left_to_play[neighbor]
            x_choice = self.play(neighbor_agent)
            y_choice = neighbor_agent.play(self)
            # todo: check if this return is handling correctly assigning the payoff to the agents
            self.fitness, neighbor_agent.fitness += distribute_payoff(x_choice, y_choice)



    def play(self, neighbor: 'Agent') -> Literal['C', 'D']:
        if self.playing_round == 1:
            return self.first_response()

        #todo: play using q/p strategy




    # todo: this is only used in the first round due to lack of information
    def first_response(self) -> Literal['C', 'D']:
        return 'C' if RANDOM_SEEDED.random() < (self.p + self.q)/2 else 'D'

    '''
    on each simulation time step, 2 neighbors are randomly picked (x and y) and calculate their individual payoff (fitness)
    player x adopts the strategy of player y with a probability given by the function adopt_strategy
    '''
    def adopt_strategy(self, fitness_y, p_y, q_y):
        adoption_probability = 1/(1 + math.exp(self.fitness - fitness_y)/SIMULATION_PARAMS['K'])

        if RANDOM_SEEDED.random() < adoption_probability:
            xi_1 = RANDOM_SEEDED.normal(0, SIMULATION_PARAMS['SIGMA']) # Mean 0, standard deviation sigma
            xi_2 = RANDOM_SEEDED.normal(0, SIMULATION_PARAMS['SIGMA'])

            self.p = p_y + xi_1
            self.q = q_y + xi_2

    def __str__(self):
        return f"Agent({self})"


@dataclass
class NeighborPlay:
    sim_step: int
    choice: Literal['C', 'D']