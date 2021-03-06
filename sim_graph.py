import sim
import json

'''
To simulate tests, all you need to change is the graph_file and the
strat_files (these are outputs of main.py. Just add the strategies you want to
test. Put in as many strategies as you want. 

The result of the simulation will be printed on the terminal with stratX being
the Xth entry in strat_files.
'''

graph_file = 'Day5Graphs/2.10.14.json'
strat_files = ['Day5Graphs/21014-deg', 'Day5Graphs/21014-test']

if __name__ == '__main__':
    with open(graph_file) as data_file:     # Get graph file as dictionary
        graph = json.load(data_file)

    file_str = graph_file.split('.')        # Get number of seeds for this graph
    num_seeds = int(file_str[1])

    nodes = {}
    for i in range(len(strat_files)):       # For each strategy get nodes
        with open(strat_files[i]) as strategy:
            seeds = sorted([next(strategy).strip() for x in xrange(num_seeds)])

        nodes['strat'+str(i)] = seeds

    print(nodes)
    res = sim.run(graph, nodes)             # Run simulation
    print("results:\n")                     # Print output
    print(res)
