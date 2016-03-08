# mas-prog-challenge
Tasked to attempt to solve the NP-hard problem of maximum acyclic subgraph. 

maximum acyclic subgraph: Given directed graph G = (V = {1,...,n},E), find an ordering of the nodes r1,...,rn (we call ri the rank of player i) that maximizes the number of forward edges.

This is an NP-hard problem with no known algorithm to solve in polynomial time. This algorithm attempts to get as many forward edges as possible.

Explanation of algorithm in algorithm_solution.py
	- Creates adjacency matrix from input graph
	- creates strongly connected components using networkx
	- for each SCC, perform hillclimbing, which divides component into permutations to hopefully find the permutation with close to the greatest number of forward edges
	- append SCC's with each other in forward order
	- count these edges and output the "max" found from the algorithm

TO RUN:
python algorithm_solution.py