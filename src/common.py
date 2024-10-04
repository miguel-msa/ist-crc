import numpy as np

#region simulation parameters

SEED = 21
RANDOM_SEEDED = np.random.default_rng(SEED)



SIMULATION_PARAMS = {
    'lattice_size': 10,
    'generations': 1000,
    'transient_period': 500,
    'b': 0.5,
    'K': 0.4,
    'SIGMA': 0.005
}
SIMULATION_PARAMS['agents'] = SIMULATION_PARAMS['lattice_size'] ** 2
SIMULATION_PARAMS['c'] = 1 - SIMULATION_PARAMS['b']

#endregion

def distribute_payoff(x_choice, y_choice):
    cost = SIMULATION_PARAMS['c']
    payoff = SIMULATION_PARAMS['b']
    reward = payoff - cost

    if x_choice == 'C' and y_choice == 'C':
        return reward, reward
    elif x_choice == 'C' and y_choice == 'D':
        return - cost, payoff
    elif x_choice == 'D' and y_choice == 'C':
        return payoff, cost
    else:
        return 0, 0 # ! check paper: 0 or punishment?

