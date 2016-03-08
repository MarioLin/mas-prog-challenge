import numpy as np
import networkx as nx
import random
import os
import sys
from random import shuffle

# Preprocessing input file to get num nodes and adjancency matrix
# Change later to loop through instances dir

output_file = open("output.out", "wb")
total_score = 0


for i in range(1, 622):
    fn = str(i) + ".in"
    print "Ranking instances/" + fn
    input_file = open("instances/" + fn, "rb").read().split("\n")
    num_nodes = int(input_file[0])
    rows = input_file[1:]

    # creating adjacency matrix
    adjacency_matrix = np.zeros(shape=(num_nodes, num_nodes))
    for i in range(0, num_nodes):
        row = rows[i].split()
        for j in range(0, num_nodes):
            adjacency_matrix[i][j] = int(row[j])


    # create adjacency lists

    # IN DEGREE
    adjacency_list_in = {}
    for i in range(1, num_nodes + 1):
        for j in range(1, num_nodes + 1):
            if j in adjacency_list_in:
                if adjacency_matrix[i-1, j-1] == 1:
                    adjacency_list_in[j].add(i)
            if j not in adjacency_list_in:
                adjacency_list_in[j] = set()
                if adjacency_matrix[i-1, j-1] == 1:
                    adjacency_list_in[j].add(i)

    # OUT DEGREE
    adjacency_list_out = {}
    for node in adjacency_list_in:
        for in_deg in adjacency_list_in[node]:
            if in_deg in adjacency_list_out:
                adjacency_list_out[in_deg].add(node)
            else:
                adjacency_list_out[in_deg] = set()
                adjacency_list_out[in_deg].add(node)


    def count_edges(arr):
        """ Counts forward and back edges in a list """
        forward_count, back_count = 0, 0
        num_nodes = len(arr)
        if len(arr) == 1:
            return 0
        for i in xrange(num_nodes):
            for j in xrange(i + 1, num_nodes):
                # checking forward edges
                if adjacency_matrix[arr[i]][arr[j]] == 1:
                    forward_count += 1
        return forward_count


    all_counts = []
    all_solutons = []
    # RANDOM RANKING
    perms = []
    counts = []
    for i in range(0, 50):
        curr = np.random.permutation(num_nodes)
        perms.append(curr)
        count = 0
        forward_count = count_edges(curr)
        # reverse aray if back > forward
        counts.append(forward_count)

    # get greatest forward edge count
    max_count_ind = counts.index(max(counts))
    # set solution to permutation with highest forward edge count
    sol = perms[max_count_ind]

    print "\nRunning Random Strategy\n---------------------------"
    print "Solution: \n", sol
    print "\nForward Edge Count: ", max(counts)

    all_counts.append(max(counts))
    all_solutons.append(sol)

    # CONNECTED COMPONENTS

    G = nx.from_numpy_matrix(adjacency_matrix, create_using=nx.DiGraph())
    G_conn = nx.strongly_connected_components(G)

    sol_scc = []
    for comp in G_conn:
        perms = []
        scc_counts = []
        for i in range(0, 100):
            curr_perm = random.sample(list(comp), len(list(comp)))
            perms.append(curr_perm)
            scc_forward_count = count_edges(curr_perm)

            scc_counts.append(scc_forward_count)

        # hill-climbing
        for i in range(0,2):
            l = list(comp)
            shuffle(l)
            output = [l[0]]
            final = [l[0]]
            curr_max = -sys.maxint - 1
            for i in l[1:]:
                for spot in range(len(final)):
                    arr = final[:spot] + [i] + final[spot:]
                    num = count_edges(arr)
                    if num > curr_max:
                        output = arr
                        curr_max = num
                final = output
                curr_max = -sys.maxint - 1
            scc_counts.append(count_edges(final))
            perms.append(final)

        # get index of max forward edge count
        scc_max_count_ind = scc_counts.index(max(scc_counts))
        # set solution to permutation with highest forward edge count
        best_sol = perms[scc_max_count_ind]
        # add sol to the front since scc functions returns component in reverse order
        sol_scc = list(best_sol) + sol_scc



    # Counting total forward edges in final solution
    forward_count_sol_scc = count_edges(sol_scc)

    all_counts.append(forward_count_sol_scc)
    all_solutons.append(sol_scc)
    print "\nRunning SCC Strategy\n---------------------------"
    print "Solution: \n", sol_scc
    print "\nForward Edge Count: ", forward_count_sol_scc


    # BEST SOLUTION

    best_ind = all_counts.index(max(all_counts))
    best_sol = all_solutons[best_ind]

    print "\nGetting Best Solution\n---------------------------"
    print "Solution: \n", best_sol
    print "\nForward Edge Count: ", all_counts[best_ind]

    total_score += all_counts[best_ind]
    print "Total Score So Far:", total_score

    # Uncomment when ready to run on all instances
    # OUTPUT
    sol_str = " ".join(str(x+1) for x in best_sol)
    output_file.write(sol_str + '\n')