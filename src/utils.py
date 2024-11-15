from typing import Dict, Literal
import networkx as nx
import matplotlib.pyplot as plt
from agent.agent import Agent
from common import RANDOM_SEEDED, SIMULATION_PARAMS
import math
import numpy as np

def init_agents() -> list[Agent]:
    agents = []
    print(f'Creating {SIMULATION_PARAMS["agents"]} agents')
    for i in range(SIMULATION_PARAMS['agents']):
        i_seed = RANDOM_SEEDED.integers(0, 101)
        j_seed = RANDOM_SEEDED.integers(0, 101)

        p = i_seed * 0.01
        q = j_seed * 0.01

        agent = Agent(i, p, q)
        agents.append(agent)
        print(f'{agent.id} - q:{round(agent.q, 3)} - p:{round(agent.p, 3)}')

    return agents

# init lattice with agents using networkx
def init_lattice(agents: list[Agent]) -> nx.Graph:
    # create a 2D grid graph
    G = nx.grid_2d_graph(SIMULATION_PARAMS['lattice_size'], SIMULATION_PARAMS['lattice_size'])

    # check if the number of agents matches the number of nodes
    if len(agents) < len(G.nodes):
        raise ValueError("Not enough agents to assign to all nodes.")

    # assign each node an Agent instance from the AGENTS list
    for idx, node in enumerate(G.nodes):
        G.nodes[node]['agent'] = agents[idx]

    # assign the agent's neighbors with a 'last play' placeholder value equal 'C'
    for node in G.nodes:
        neighbors = G.neighbors(node)
        for n in neighbors:
            neighbor_agent: Agent = G.nodes[n]['agent']
            G.nodes[node]['agent'].last_play_by_neighbor[neighbor_agent.id] = 'C'
    return G


def distribute_payoff(x_choice, y_choice):
    cost = SIMULATION_PARAMS['c']
    payoff = SIMULATION_PARAMS['b']
    reward = payoff - cost

    if x_choice == 'C' and y_choice == 'C':
        return reward, reward
    elif x_choice == 'C' and y_choice == 'D':
        return - cost, payoff
    elif x_choice == 'D' and y_choice == 'C':
        return payoff, - cost
    else:
        return 0, 0 # ! check paper: 0 or punishment?

def pick_two_random_neighboring_nodes(G):
    random_node = tuple(int(x) for x in RANDOM_SEEDED.choice(list(G.nodes)))
    neighbors = list(G.neighbors(random_node))

    neighbor_index = RANDOM_SEEDED.choice(len(neighbors))
    neighbor = neighbors[neighbor_index]

    return random_node, neighbor

def draw_graph(g: nx.Graph):
    pos = dict((n, n) for n in g.nodes())

    nx.draw(g, pos, with_labels=False, node_size=300, node_color='lightblue',
            font_size=8, font_color='black')

    plt.show()


class SimulationResult():
    def __init__(self, total_sims: int, total_play: int, coop_ratio_sum: float, p: float, q: float):
        self.total_sims = total_sims
        self.total_play = total_play
        self.coop_ratio_sum = coop_ratio_sum
        self.p = p
        self.q = q

    def getAvgCoop(self):
        return self.coop_ratio_sum/self.total_sims

    def getAvgP(self):
        return self.p/self.total_sims

    def getAvgQ(self):
        return self.q/self.total_sims
