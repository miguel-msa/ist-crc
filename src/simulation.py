from typing import List
from utils import SIMULATION_PARAMS, init_agents, init_lattice, draw_graph, pick_two_random_neighboring_nodes
from agent.agent import Agent


'''
# for the simulation divide by a factor of 10 everything (lattice: 10x10; 1000 generations; 10000 generations to follow, transient period: 500 generations)
simulation configuration are @ common.py
'''
def simulate():
    # init agent with random values of p and q where p = i*0.01 and q = i*0.01 for i,j  in range(1, 101) random for each agent
    agents = init_agents()

    # init lattice with agents
    G = init_lattice(agents)

    # ! TEST: draw the graph
    # draw_graph(G)

    for _ in range(SIMULATION_PARAMS['generations']):
        # for each agent, play with all its neighbors
        for node in G.nodes:
            agent: Agent = G.nodes[node]['agent']
            neighbors = G.neighbors(node)

            neighbor_agents: List[Agent] = list(G.nodes[n]['agent'] for n in neighbors)

            agent.play_with_neighbors(neighbor_agents)

        # randomly pick 2 neighbors to, with a probability, adopt the strategy of the other
        node_x, node_y = pick_two_random_neighboring_nodes(G)

        node_x_agent: Agent = G.nodes[node_x]['agent']
        node_y_agent: Agent = G.nodes[node_y]['agent']

        node_x_agent.adopt_strategy(node_y_agent.fitness, node_y_agent.p, node_y_agent.q)

    for agent in agents:
        print(f'Agent {agent.id} with fitness {agent.fitness}, p: {agent.p}, q: {agent.q}')

if __name__ == '__main__':
    simulate()

