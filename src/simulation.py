from utils import SIMULATION_PARAMS, init_agents, init_lattice, draw_graph


'''
# for the simulation divide by a factor of 10 everything (lattice: 10x10; 1000 generations; 10000 generations to follow, transient period: 500 generations)
simulation configuration are @ common.py
'''
def simulate():
    # init agent with random values of p and q where p = i*0.01 and q = i*0.01 for i,j  in range(1, 101) random for each agent
    agents = init_agents()

    # init lattice with agents
    graph = init_lattice(agents)

    # draw the graph
    draw_graph(graph)

    # for step in range(SIMULATION_PARAMS['generations']):
    #     # for each agent, play with all its neighbors
    #     graph.neighbors()


simulate()

