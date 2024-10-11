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
        self.fitness = 0 # todo: increase on every game
        self.last_play_by_neighbor: Dict[int, NeighborPlay] = {}
        self.playing_round = 0
        self.play_flag = 0
        self.cooperate_flag = 0
        self.defect_flag = 0

    def play_with_neighbors(self, neighbors_to_play: List['Agent']):
        self.playing_round += 1

        # print(f'Agent {self.id} on round {self.playing_round} with {len(neighbors_to_play)} neighbors')
        # for neighbor in neighbors_to_play:
        #     print(f'{neighbor.id} | {neighbor.playing_round}')

        # filter out neighbors that have already played with this agent
        neighbors_left_to_play = list(filter(lambda n: self.playing_round > n.playing_round, neighbors_to_play))
        '''
        if len(neighbors_left_to_play) > 0:
            print(f'Agent {self.id} on round {self.playing_round} will play with {len(neighbors_left_to_play)} neighbors')
            for neighbor in neighbors_left_to_play:
                print(f'{neighbor.id} | {neighbor.playing_round}')
        '''

        for idx, _ in enumerate(neighbors_left_to_play):
            neighbor_agent: Agent = neighbors_left_to_play[idx]
            x_choice = self.play(neighbor_agent)
            y_choice = neighbor_agent.play(self)


            self.store_neighbor_choice(neighbor_agent.id, y_choice)
            neighbor_agent.store_neighbor_choice(self.id, x_choice)

            # todo: check if this return is handling correctly assigning the payoff to the agents
            from utils import distribute_payoff
            self_payoff, neighbor_payoff = distribute_payoff(x_choice, y_choice)
            #print(f'{self_payoff} | {neighbor_payoff}')
            self.fitness += self_payoff
            neighbor_agent.fitness += neighbor_payoff



    def play(self, neighbor: 'Agent') -> Literal['C', 'D']:

        if self.playing_round == 1:
            self.play_flag += 1
            first_response = self.first_response()
            if(first_response == 'C'):
                self.cooperate_flag += 1
            elif(first_response == 'D'):
                self.defect_flag += 1

            return first_response
            # get the last choice the neighbord made when playing with this agent
        last_neighbor_choice = self.last_play_by_neighbor[neighbor.id]

        if last_neighbor_choice is None:
            self.play_flag += 1
            first_response = self.first_response()
            if(self.playing_round >= SIMULATION_PARAMS['transient_period']):
                if(first_response == 'C'):
                    self.cooperate_flag += 1
                elif(first_response == 'D'):
                    self.defect_flag += 1

            return first_response
        
        if last_neighbor_choice == 'C':
            self.play_flag += 1
            if(RANDOM_SEEDED.random() < self.p):
                if(self.playing_round >= SIMULATION_PARAMS['transient_period']):
                    self.cooperate_flag += 1
                return 'C'
            else:
                if(self.playing_round >= SIMULATION_PARAMS['transient_period']):
                    self.defect_flag += 1
                return 'D'
        elif last_neighbor_choice == 'D':
            self.play_flag += 1
            if (RANDOM_SEEDED.random() < self.q):
                if(self.playing_round >= SIMULATION_PARAMS['transient_period']):
                    self.cooperate_flag += 1
                return 'C'  
            else:
                if(self.playing_round >= SIMULATION_PARAMS['transient_period']):
                    self.defect_flag += 1
                return 'D'




    # todo: this is only used in the first round due to lack of information
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