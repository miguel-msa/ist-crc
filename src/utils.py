from typing import Dict, Literal
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

    # assign the agent's neighbors with a 'last play' placeholder value equal 'C'
    for node in G.nodes:
        neighbors = G.neighbors(node)
        for n in neighbors:
            neighbor_agent: Agent = G.nodes[n]['agent']
            G.nodes[node]['agent'].last_play_by_neighbor[neighbor_agent.id] = 'C'
    return G


# todo: review this payoff matrix and the way it is calculated!
'''def distribute_payoff(x_choice, y_choice):
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
'''

def pick_two_random_neighboring_nodes(G):
    random_node = RANDOM_SEEDED.choice(list(G.nodes))
    print(random_node)

    neighbors = list(G.neighbors(random_node))

    neighbor_index = RANDOM_SEEDED.choice(len(neighbors))
    neighbor = neighbors[neighbor_index]

    return random_node, neighbor

def draw_graph(g: nx.Graph):
    pos = dict((n, n) for n in g.nodes())

    nx.draw(g, pos, with_labels=False, node_size=300, node_color='lightblue',
            font_size=8, font_color='black')

    plt.show()