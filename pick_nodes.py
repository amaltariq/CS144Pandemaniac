import networkx as nx
import heapq
import operator 

def pick_seeds(in_graph, num_seeds):
    if num_seeds < 3000:
        seeds = pick_nodes_closeness(in_graph, num_seeds)
    else:
       seeds = pick_nodes_degree(in_graph, num_seeds)
       #seeds = pick_nodes_closeness(in_graph, num_seeds)
    return seeds

def output_nodes(list_nodes, output_file):
    fo = open(output_file, "wb")

    for i in range(50):
        for node in list_nodes:
            fo.write("%s\n" % str(node))

def pick_nodes_betweenness(in_graph, num_vals):
     # Dictionary of nodes and betweenness values
    betweenness_values = nx.betweenness_centrality(in_graph)

    list_betweenness = betweenness_values.items()   # Convert to tuple list

    # Get top betweenness ranked nodes and values
    top_between = heapq.nlargest(num_vals, list_betweenness,
                                 key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_between]     # Get only node IDs

    return top_nodes

# this method lost against highest degree
def pick_most_between_and_neighbors(in_graph, num_seeds):
    most_bw_node = pick_nodes_betweenness(in_graph, 1)
    top_nodes = []
    top_nodes.append(most_bw_node[0])
    bw_neighbors = in_graph.neighbors(most_bw_node[0])

    
    for i in range(num_seeds-1):
        if i < len(bw_neighbors):
            top_nodes.append(bw_neighbors[i])
        else:
            break
    
    assert(len(top_nodes) == num_seeds)
    return top_nodes

def pick_nodes_degree(in_graph, num_vals):
    degree_values = nx.degree_centrality(in_graph)

    list_degree = degree_values.items()

    top_degree = heapq.nlargest(num_vals, list_degree,
                                key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_degree]

    return top_nodes

# this has around 90% of the same nodes as highest degree method, wins but
# might be random
def pick_nodes_closeness(in_graph, num_seeds):
    closeness_values = nx.closeness_centrality(in_graph)

    list_closeness = closeness_values.items()

    top_close = heapq.nlargest(num_seeds, list_closeness,
                               key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_close]

    return top_nodes

# totally unsuccessful (tried 1/3, 1/3, 1/3 and 1/2, 1/2, 0, both lost to
# highest degree)
def mixed_strategy(in_graph, num_seeds):
    deg_nodes = sorted(pick_nodes_degree(in_graph, 2*num_seeds))
    between_nodes = sorted(pick_nodes_betweenness(in_graph, 2*num_seeds))
    close_nodes = sorted(pick_nodes_closeness(in_graph, 2*num_seeds))

    num_deg = num_seeds/3
    num_bw = num_seeds/3
    num_close = num_seeds - num_deg - num_bw

    top_nodes = []

    j = 0
    for i in range(num_deg):
        top_nodes.append(deg_nodes[j])
        j += 1

    j = 0
    for i in range(num_bw):
        while between_nodes[j] in top_nodes:
            j += 1
            if j > len(between_nodes):
                print("j too large, between_nodes")
        top_nodes.append(between_nodes[j])
        j += 1

    j = 0
    for i in range(num_close):
        while close_nodes[j] in top_nodes:
            j += 1
            if j > len(close_nodes):
                print("j too large, close_nodes")
        top_nodes.append(between_nodes[j])
        j+= 1

    assert(len(top_nodes) == num_seeds)
    return top_nodes


