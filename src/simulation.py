from utils import SIMULATION_PARAMS, init_agents, init_lattice, draw_graph, distribute_payoff
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

    # TEST: draw the graph
    draw_graph(G)

    for step in range(SIMULATION_PARAMS['generations']):
        # for each agent, play with all its neighbors
        for node in G.nodes:
            agent: Agent = G.nodes[node]['agent']
            neighbors = G.neighbors(node)

            # todo: track which agents have already played with each other
            for neighbor in neighbors:
                neighbor_agent: Agent = G.nodes[neighbor]['agent']

                # todo: add a way to track previous choice between agents
                x_choice = agent.play(neighbor_agent)
                y_choice = neighbor_agent.play(agent)

                agent.fitness, neighbor.fitness += distribute_payoff(x_choice, y_choice)





simulate()

