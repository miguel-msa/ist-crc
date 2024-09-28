import math
from utils import RANDOM_SEEDED, SIMULATION_PARAMS

class Agent:
    def __init__(self, id: int, b: int, p: int, q: int):
        self.id = id
        self.b = b
        self.p = p
        self.q = q
        self.fitness = 0 # todo: increase on every game
        self.neighbors = {}

    # neighbors = {
    #     2: [],
    #     5: [True, True],
    # }

    # todo: this is only used in the first round due to lack of information
    def first_response(self) -> float:
        # cooperate -> (self.p + self.q)/2
        # defect -> [1 - (self.p + self.q)/2]
        return

    def adopt_strategy(self, fitness_y, p_y, q_y):
        adoption_probability = 1/(1 + math.exp(self.fitness - fitness_y)/SIMULATION_PARAMS['K'])

        if RANDOM_SEEDED.random() < adoption_probability:
            xi_1 = RANDOM_SEEDED.normal(0, SIMULATION_PARAMS['SIGMA']) # Mean 0, standard deviation sigma
            xi_2 = RANDOM_SEEDED.normal(0, SIMULATION_PARAMS['SIGMA'])

            self.p = p_y + xi_1
            self.q = q_y + xi_2

    def __str__(self):
        return f"Agent({self})"


