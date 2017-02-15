import networkx as nx
import heapq
import operator 

def pick_seeds(in_graph, num_seeds):
    # Dictionary of nodes and betweenness values
    betweenness_values = nx.betweenness_centrality(in_graph)

    list_betweenness = betweenness_values.items()   # Convert to tuple list

    # Get top betweenness ranked nodes and values
    top_between = heapq.nlargest(num_seeds, list_betweenness,
                                 key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_between]     # Get only node IDs

    return top_nodes


def output_nodes(list_nodes, output_file):
    fo = open(output_file, "wb")

    for i in range(50):
        for node in list_nodes:
            fo.write("%s\n" % str(node))
