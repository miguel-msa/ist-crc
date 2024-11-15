import numpy as np
import random

#region simulation parameters

SEED = random.seed() #400 #21
RANDOM_SEEDED = np.random.default_rng(SEED)

SIMULATION_PARAMS = {
    'lattice_size': 30,
    'b': 1.1,
    'K': 0.4,
    'SIGMA': 0.005
}
SIMULATION_PARAMS['agents'] = SIMULATION_PARAMS['lattice_size'] ** 2
SIMULATION_PARAMS['c'] = SIMULATION_PARAMS['b'] - 1
SIMULATION_PARAMS['generations'] = (SIMULATION_PARAMS['lattice_size'] ** 2) * 10
SIMULATION_PARAMS['transient_period'] = SIMULATION_PARAMS['lattice_size'] ** 2

#endregion
