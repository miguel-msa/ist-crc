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