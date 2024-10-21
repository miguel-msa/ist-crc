from typing import List
from utils import SIMULATION_PARAMS, init_agents, init_lattice, draw_graph, pick_two_random_neighboring_nodes, SimulationResult
from agent.agent import Agent
from common import SEED
import matplotlib.pyplot as plt

'''
# for the simulation divide by a factor of 10 everything (lattice: 10x10; 1000 generations; 10000 generations to follow, transient period: 500 generations)
simulation configuration are @ common.py
'''
TOTAL_SIMS = 1 #10
PAYOFFS = [1.001, 1.2, 1.4, 1.6, 1.8, 2.0]
#PAYOFFS = [1.001, 1.2]

SIMULATION_RESULTS = {}


def simulate():

    p_avg_in_generation = 0
    q_avg_in_generation = 0 
    p_avg_generation = []
    q_avg_generation = []
    p_avg_simulation = [None] * TOTAL_SIMS
    q_avg_simulation = [None] * TOTAL_SIMS
    p_final_iter_sum = 0
    q_final_iter_sum = 0
    p_avg_simulation_final = []
    q_avg_simulation_final = []
    EXTRA_SIMULATION_RESULTS_P = {}
    EXTRA_SIMULATION_RESULTS_Q = {}

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

                for agent in agents:
                    #agent: Agent = G.nodes[node]['agent']
                    p_avg_in_generation += agent.p
                    q_avg_in_generation += agent.q
                
                p_avg_in_generation = (p_avg_in_generation/(SIMULATION_PARAMS['lattice_size'] ** 2))
                q_avg_in_generation = (q_avg_in_generation/(SIMULATION_PARAMS['lattice_size'] ** 2))

                # Mean value of every agents p and q in all generations [size 100]
                p_avg_generation.append(p_avg_in_generation)
                q_avg_generation.append(q_avg_in_generation)
                p_avg_in_generation = 0
                q_avg_in_generation = 0


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
            if b == PAYOFFS[0] or b == PAYOFFS[-1]:
                #print(sim_iteration)
                # Mean value of every agents p and q in all generations, organized per iteration [size 10*100]
                p_avg_simulation[sim_iteration] = p_avg_generation
                q_avg_simulation[sim_iteration] = q_avg_generation

            if b == PAYOFFS[0] or b == PAYOFFS[-1]:
                '''
                p_avg_simulation_final = p_avg_simulation[sim_iteration]
                print(p_avg_simulation_final)
                q_avg_simulation_final += q_avg_simulation[sim_iteration]
                '''
                for gen in range(SIMULATION_PARAMS['generations']):
                    for iter in range(TOTAL_SIMS):
                        p_final_iter_sum += p_avg_simulation[iter][gen]
                        q_final_iter_sum += q_avg_simulation[iter][gen]
                        #print("AQUI: ", p_avg_simulation_final)
                    p_avg_simulation_final.append(p_final_iter_sum / TOTAL_SIMS)
                    q_avg_simulation_final.append(q_final_iter_sum / TOTAL_SIMS)
                    p_final_iter_sum = 0
                    q_final_iter_sum = 0



        if b == PAYOFFS[0]:
            EXTRA_SIMULATION_RESULTS_P[0] = p_avg_simulation_final
            EXTRA_SIMULATION_RESULTS_Q[0] = q_avg_simulation_final
        elif b == PAYOFFS[-1]:
            EXTRA_SIMULATION_RESULTS_P[1] = p_avg_simulation_final
            EXTRA_SIMULATION_RESULTS_Q[1] = q_avg_simulation_final
        '''
        else:
            print(b)
            print("Isto não é suposto acontecer")
            exit()
        '''
            
        for sim_iteration in range(TOTAL_SIMS):
            p_avg_simulation_final = []
            q_avg_simulation_final = []




    avg_coop_arr = list()
    for k, sim_result in SIMULATION_RESULTS.items():
        sim_result: SimulationResult
        avg_coop_arr.append(sim_result.getAvgCoop())

    print(avg_coop_arr)

    plt.plot(PAYOFFS, avg_coop_arr)

    # Plot for Average Cooperation
    plt.figure(figsize=(8, 6))
    plt.plot(PAYOFFS, avg_coop_arr, label='Average Cooperation', color='blue', linewidth=2)
    plt.title('Average Cooperation vs Temptation to Defect (b)', fontsize=16)
    plt.xlabel('b (Temptation to Defect)', fontsize=14)
    plt.ylabel('Average Cooperation', fontsize=14)
    plt.ylim(0, 1)
    plt.xlim(1, 2)
    plt.legend()
    plt.grid(False)
    plt.show()
    plt.figure(figsize=(8, 6))

    # Prepare the data
    avg_p_arr = [SIMULATION_RESULTS[b].getAvgP() for b in PAYOFFS]
    avg_q_arr = [SIMULATION_RESULTS[b].getAvgQ() for b in PAYOFFS]

    # Plot p (blue) and q (red) with markers
    plt.plot(PAYOFFS, avg_p_arr, label='p', color='blue', linestyle='-', marker='o', markersize=5)
    plt.plot(PAYOFFS, avg_q_arr, label='q', color='red', linestyle='-', marker='^', markersize=5)
    plt.title('Average p and q at Stationary State', fontsize=16)
    plt.xlabel('b (Temptation to Defect)', fontsize=14)
    plt.ylabel('Average at Stationary State', fontsize=14)
    plt.ylim(0, 1)
    plt.xlim(1, 2)
    plt.legend()
    plt.grid(False)
    plt.show()

    # Plot the average p and q values over all generations for b == PAYOFFS[0]
    plt.plot(range(SIMULATION_PARAMS['generations']), EXTRA_SIMULATION_RESULTS_P[0], label = 'p', color = 'blue', linestyle = '-')
    plt.plot(range(SIMULATION_PARAMS['generations']), EXTRA_SIMULATION_RESULTS_Q[0], label = 'q', color = 'red', linestyle = '-')
    plt.title('Average p and q over all generations, b = 1.001', fontsize = 16)
    #plt.xlabel()
    #plt.ylabel()
    plt.ylim(0, 1)
    plt.xlim(0, SIMULATION_PARAMS['generations'])
    plt.legend()
    plt.grid(False)
    plt.show()

    # Plot the average p and q values over all generations for b == PAYOFFS[-1]
    plt.plot(range(SIMULATION_PARAMS['generations']), EXTRA_SIMULATION_RESULTS_P[1], label = 'p', color = 'blue', linestyle = '-')
    plt.plot(range(SIMULATION_PARAMS['generations']), EXTRA_SIMULATION_RESULTS_Q[1], label = 'q', color = 'red', linestyle = '-')
    plt.title('Average p and q over all generations, b = 2', fontsize = 16)
    #plt.xlabel()
    #plt.ylabel()
    plt.ylim(0, 1)
    plt.xlim(0, SIMULATION_PARAMS['generations'])
    plt.legend()
    plt.grid(False)
    plt.show()




if __name__ == '__main__':
    simulate()


