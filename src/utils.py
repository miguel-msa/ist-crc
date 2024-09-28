import networkx as nx
import matplotlib.pyplot as plt
from agent.agent import Agent
from common import RANDOM_SEEDED, SIMULATION_PARAMS

def init_agents() -> list[Agent]:
    agents = []
    for i in range(SIMULATION_PARAMS['agents']):
        i = RANDOM_SEEDED.integers(1, 101)
        j = RANDOM_SEEDED.integers(1, 101)

        p = i * 0.01
        q = j * 0.01

        agent = Agent(i, p, q)
        agents.append(agent)
    return agents

# init lattice with agents using networkx
def init_lattice(agents: list[Agent]) -> nx.Graph:
    # create a 2D grid graph
    G = nx.grid_2d_graph(SIMULATION_PARAMS['lattice_size'], SIMULATION_PARAMS['lattice_size'])

    # assign each node an Agent instance from the AGENTS list
    for idx, node in enumerate(G.nodes):
        G.nodes[node]['agent'] = agents[idx]

    return G


def simulate_step():
    # todo: each agent plays with all its neighbors
    pass
    # todo: randomly pick 2 neighbors to, with a probability, adopt the strategy of the other
    pass

# todo: review this payoff matrix and the way it is calculated!
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

def draw_graph(g: nx.Graph):
    pos = dict((n, n) for n in g.nodes())

    nx.draw(g, pos, with_labels=False, node_size=300, node_color='lightblue',
            font_size=8, font_color='black')

    plt.show()