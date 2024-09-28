import math
import random
import numpy as np
from agent.agent import Agent

#region simulation parameters

SEED = 21
RANDOM_SEEDED = np.random.default_rng(SEED)

SIMULATION_PARAMS = {
    'lattice_size': 10,
    'generations': 1000,
    'transient_period': 500,
    'agents': 100,
    'K': 0.4,
    'SIGMA': 0.005
}

#todo: define the payoff matrix

#endregion

def simulate_step():
    # todo: each agent plays with all its neighbors
    pass
    # todo: randomly pick 2 neighbors to, with a probability, adopt the strategy of the other
    pass

'''
on each simulation time step, 2 neighbors are randomly picked (x and y) and calculate their individual payoff (fitness)
player x adopts the strategy of player y with a probability given by the function adopt_strategy
'''
# todo: how to calculate the fitness of a player
def should_adopt_strategy(fitness_x, fitness_y):
    return random.random() < (1/(1 + math.exp(fitness_x - fitness_y)/K))

def adopt_strategy(fitness_x, fitness_y, x: Agent, y):
    adoption_probability = 1/(1 + math.exp(fitness_x - fitness_y)/K)

    if random.random() < adoption_probability:
        xi_1 = np.random.normal(0, SIGMA) # Mean 0, standard deviation sigma
        xi_2 = np.random.normal(0, SIGMA)

        x.p = y.p + xi_1
        x.q = y.q + xi_2