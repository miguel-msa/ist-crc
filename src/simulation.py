from typing import List
from utils import SIMULATION_PARAMS, init_agents, init_lattice, draw_graph, pick_two_random_neighboring_nodes, SimulationResult
from agent.agent import Agent
from common import SEED
import matplotlib.pyplot as plt

'''
# for the simulation divide by a factor of 10 everything (lattice: 10x10; 1000 generations; 10000 generations to follow, transient period: 500 generations)
simulation configuration are @ common.py
'''
TOTAL_SIMS = 3
#PAYOFFS = [1.001, 1.2, 1.4, 1.6, 1.8, 2.0]
PAYOFFS = [1.001, 1.2]
SIMULATION_RESULTS = {}
def simulate():
    # init agent with random values of p and q where p = i*0.01 and q = i*0.01 for i,j  in range(1, 101) random for each agent
    for b in PAYOFFS:
        SIMULATION_RESULTS[b] = SimulationResult(TOTAL_SIMS, 0, 0, 0, 0)

        SIMULATION_PARAMS['b'] = b
        SIMULATION_PARAMS['c'] = b - 1

        for sim_iteration in range(TOTAL_SIMS):
            agents = init_agents()


            total_plays = 0
            total_cooperates = 0
            total_defects = 0
            average_p = 0
            average_q = 0

            # init lattice with agents
            G = init_lattice(agents)

            # ! TEST: draw the graph
            #draw_graph(G)

            for generation in range(SIMULATION_PARAMS['generations']):
                if(generation % 100 == 0):
                    print(generation)
                # for each agent, play with all its neighbors
                for node in G.nodes:
                    agent: Agent = G.nodes[node]['agent']
                    neighbors = G.neighbors(node)

                    neighbor_agents: List[Agent] = list(
                            G.nodes[n]['agent'] for n in neighbors)

                    agent.play_with_neighbors(neighbor_agents)
                    if (generation >= SIMULATION_PARAMS['transient_period']):
                        total_plays += agent.play_flag
                        total_cooperates += agent.cooperate_flag
                        total_defects += agent.defect_flag
                    agent.play_flag = 0
                    agent.cooperate_flag = 0
                    agent.defect_flag = 0
                    # randomly pick 2 neighbors to, with a probability, adopt the strategy of the other
                    node_x, node_y = pick_two_random_neighboring_nodes(G)

                    node_x_agent: Agent = G.nodes[node_x]['agent']
                    node_y_agent: Agent = G.nodes[node_y]['agent']

                    node_x_agent.adopt_strategy(node_y_agent.fitness, node_y_agent.p, node_y_agent.q)

            '''
            # randomly pick 2 neighbors to, with a probability, adopt the strategy of the other
            node_x, node_y = pick_two_random_neighboring_nodes(G)

                    node_x_agent: Agent = G.nodes[node_x]['agent']
                    node_y_agent: Agent = G.nodes[node_y]['agent']

            node_x_agent.adopt_strategy(node_y_agent.fitness, node_y_agent.p, node_y_agent.q)
            '''

            '''
            for node in G.nodes:
                agent: Agent = G.nodes[node]['agent']
                if agent.fitness < 0:
                    agent.fitness = 0
            '''

            #node_x_agent.fitness = 0
            #node_y_agent.fitness = 0

            for agent in agents:
                print(f'''Agent {agent.id} with
                      fitness {agent.fitness}, p: {agent.p}, q: {agent.q}''')
                average_p += agent.p
                average_q += agent.q

            average_p = average_p/(SIMULATION_PARAMS['lattice_size']**2)
            average_q = average_q/(SIMULATION_PARAMS['lattice_size']**2)

            CD_check = total_cooperates + total_defects

            print(f'b: {b} | simulation: {sim_iteration + 1}\n-------------------')
            print("Total plays:", total_plays)
            print("Total cooperates:", total_cooperates)
            print("CD_check:", CD_check)
            print("Average p:", average_p)
            print("Average q:", average_q)

            cooperation_ratio = total_cooperates/total_plays
            print(f'Cooperation Ratio: {cooperation_ratio}')

            SIMULATION_RESULTS[b].plays_count = total_plays
            SIMULATION_RESULTS[b].coop_ratio_sum += cooperation_ratio
            SIMULATION_RESULTS[b].p += average_p
            SIMULATION_RESULTS[b].q += average_q

    avg_coop_arr = list()
    for k, sim_result in SIMULATION_RESULTS.items():
        sim_result: SimulationResult
        avg_coop_arr.append(sim_result.getAvgCoop())

    print(avg_coop_arr)

    plt.plot(PAYOFFS, avg_coop_arr)


if __name__ == '__main__':
    simulate()


