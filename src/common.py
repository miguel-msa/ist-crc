import numpy as np

#region simulation parameters

SEED = 400 #21
RANDOM_SEEDED = np.random.default_rng(SEED)

SIMULATION_PARAMS = {
    'lattice_size': 10,
    'generations': 1000,
    'transient_period': 500,
    'b': 2,
    #'b': [1.001, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
    'K': 0.4,
    'SIGMA': 0.005
}
SIMULATION_PARAMS['agents'] = SIMULATION_PARAMS['lattice_size'] ** 2
SIMULATION_PARAMS['c'] = SIMULATION_PARAMS['b'] - 1

#endregion