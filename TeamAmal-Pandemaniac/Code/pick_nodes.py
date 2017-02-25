import networkx as nx
import heapq
import operator
from parallel_betweenness import betweenness_centrality_parallel 
#p1 - 1, 7, 3, 3 - won
#p2 - 1, 10, 3, 5 - won
#p3 - 1, 3, 5, 8 - lost
#p4 - 1, 10, 2, 3
def pick_seeds(in_graph, num_seeds):
    if nx.number_of_nodes(in_graph) < 3000:
        print('Weighted seeds')
        seeds = weighted_seeds(in_graph, num_seeds, 1.0, 10.0, 3.0, 5.0)
    else:
        print('Pagerank')
        seeds = pick_nodes_pagerank(in_graph, num_seeds)
    
    # various strategies we tried at some point
    #seeds = pick_nodes_betweenness(in_graph, num_seeds)
    #seeds = pick_nodes_pagerank(in_graph, num_seeds)
    #seeds = pick_nodes_clustering(in_graph, num_seeds)
    #seeds = pick_closeness_degree(in_graph, num_seeds,1)
    #seeds = pick_nodes_degree(in_graph, num_seeds)
    #seeds = weighted_seeds(in_graph, num_seeds, 1.0, 10.0, 2.0, 3.0)

    return seeds

def output_nodes(list_nodes, output_file):
    fo = open(output_file, "wb")

    for i in range(50):
        for node in list_nodes:
            fo.write("%s\n" % str(node))

def pick_closeness_degree(in_graph, num_seeds, num_deg):
    highest_deg = pick_nodes_degree(in_graph, num_seeds)
    closeness_nodes = pick_nodes_closeness(in_graph, 2*num_seeds)

    seeds = highest_deg[0:num_deg]

    for n in closeness_nodes:
        if len(seeds) >= num_seeds:
            break

        if n not in seeds:
            seeds.append(n)

    return seeds

def pick_nodes_clustering(in_graph, num_vals):
    clust_vals = nx.clustering(in_graph)
    list_clust = clust_vals.items()
    top_clust = heapq.nlargest(num_vals, list_clust, key=operator.itemgetter(1))
    top_nodes = [tup[0] for tup in top_clust]
    return top_nodes

def pick_nodes_eigenvector(in_graph, num_seeds):
    ev_values = nx.eigenvector_centrality(in_graph)

    list_ev = ev_values.items()

    top_ev = heapq.nlargest(num_seeds, list_ev,
                               key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_ev]

    return top_nodes

def pick_nodes_pagerank(in_graph, num_seeds):
    pr_values = nx.pagerank(in_graph)

    list_pr = pr_values.items()

    top_pr = heapq.nlargest(num_seeds, list_pr,
                               key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_pr]

    return top_nodes

def weighted_seeds(in_graph, num_seeds, w_d, w_c, w_nd, w_nc):
    node_degree = nx.degree_centrality(in_graph)

    node_closeness = nx.closeness_centrality(in_graph)

    adj_list = nx.to_dict_of_lists(in_graph)

    sum_neighbor_degree = {}
    sum_neighbor_close = {}
    norm_deg_nbr = 0
    norm_close_nbr = 0
    for n in adj_list.keys():
        nbr_list = adj_list[n]
        if len(nbr_list) > 1:
            sum_deg = 0
            sum_close = 0
            for nbr in nbr_list:
                sum_deg += node_degree[nbr]
                sum_close += node_closeness[nbr]
            sum_neighbor_degree[n] = sum_deg
            sum_neighbor_close[n] = sum_close
            norm_deg_nbr += sum_deg
            norm_close_nbr += sum_close
            
    norm_deg = sum(node_degree.values())
    norm_close = sum(node_closeness.values())



    scores = []
    for n in sum_neighbor_degree.keys():
        val = w_d * node_degree[n] / norm_deg + w_c * node_closeness[n]/norm_close \
                    + w_nd * sum_neighbor_degree[n]/norm_deg_nbr \
                    + w_nc * sum_neighbor_close[n]/norm_close_nbr
        scores.append((n, val))

    top_scores = heapq.nlargest(num_seeds, scores,
                                 key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_scores]

    return top_nodes

def weighted_seeds_with_cluster(in_graph, num_seeds, w_d, w_c, w_cl, w_nd, w_nc, w_ncl):
    node_degree = nx.degree_centrality(in_graph)

    node_closeness = nx.closeness_centrality(in_graph)
    node_cluster = nx.clustering(in_graph)

    adj_list = nx.to_dict_of_lists(in_graph)

    sum_neighbor_degree = {}
    sum_neighbor_close = {}
    sum_neighbor_cluster = {}

    norm_deg_nbr = 0
    norm_close_nbr = 0
    norm_clust_nbr = 0

    for n in adj_list.keys():
        nbr_list = adj_list[n]
        if len(nbr_list) > 1:
            sum_deg = 0
            sum_close = 0
            sum_clust = 0

            for nbr in nbr_list:
                sum_deg += node_degree[nbr]
                sum_close += node_closeness[nbr]
                sum_clust += node_cluster[nbr]
            sum_neighbor_degree[n] = sum_deg
            sum_neighbor_close[n] = sum_close
            sum_neighbor_cluster[n] = sum_clust
            norm_deg_nbr += sum_deg
            norm_close_nbr += sum_close
            norm_clust_nbr += sum_clust
            
    norm_deg = sum(node_degree.values())
    norm_close = sum(node_closeness.values())

    norm_deg = max(node_degree.values())
    norm_close = max(node_closeness.values())
    norm_clust = max(node_cluster.values())
    norm_deg_nbr = max(sum_neighbor_degree.values())
    norm_close_nbr = max(sum_neighbor_close.values())
    norm_clust_nbr = max(sum_neighbor_cluster.values())

    scores = []
    for n in sum_neighbor_degree.keys():
        val = w_d * node_degree[n] / norm_deg + w_c * node_closeness[n]/norm_close \
                    + w_cl * node_cluster[n] / norm_deg \
                    + w_nd * sum_neighbor_degree[n]/norm_deg_nbr \
                    + w_nc * sum_neighbor_close[n]/norm_close_nbr \
                    + w_ncl * sum_neighbor_cluster[n]/norm_close_nbr
        scores.append((n, val))

    top_scores = heapq.nlargest(num_seeds, scores,
                                 key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_scores]

    return top_nodes

def weighted_seeds_with_bw(in_graph, num_seeds, w_d, w_c, w_b, w_nd, w_nc, w_nb):
    node_degree = nx.degree_centrality(in_graph)

    node_closeness = nx.closeness_centrality(in_graph)

    node_bwness = betweenness_centrality_parallel(in_graph)

    adj_list = nx.to_dict_of_lists(in_graph)

    sum_neighbor_degree = {}
    sum_neighbor_close = {}
    sum_neighbor_bw = {}
    norm_deg_nbr = 0
    norm_close_nbr = 0
    norm_bw_nbr = 0
    for n in adj_list.keys():
        nbr_list = adj_list[n]
        if len(nbr_list) > 1:
            sum_deg = 0
            sum_close = 0
            sum_bw = 0
            for nbr in nbr_list:
                sum_deg += node_degree[nbr]
                sum_close += node_closeness[nbr]
                sum_bw += node_bwness[nbr]
            sum_neighbor_degree[n] = sum_deg
            sum_neighbor_close[n] = sum_close
            sum_neighbor_bw[n] = sum_bw
            norm_deg_nbr += sum_deg
            norm_close_nbr += sum_close
            norm_bw_nbr += sum_bw
            
    norm_deg = sum(node_degree.values())
    norm_close = sum(node_closeness.values())
    norm_bw = sum(node_bwness.values())

    scores = []
    for n in sum_neighbor_degree.keys():
        val = w_d * node_degree[n] / norm_deg + w_c * node_closeness[n]/norm_close \
                    + w_b * node_bwness[n] / norm_bw \
                    + w_nd * sum_neighbor_degree[n]/norm_deg_nbr \
                    + w_nc * sum_neighbor_close[n]/norm_close_nbr \
                    + w_nb * sum_neighbor_bw[n]/norm_bw_nbr
        scores.append((n, val))

    top_scores = heapq.nlargest(num_seeds, scores,
                                 key=operator.itemgetter(1))

    top_nodes = [tup[0] for tup in top_scores]

    return top_nodes

def pick_nodes_betweenness(in_graph, num_vals):
     # Dictionary of nodes and betweenness values
    #betweenness_values = nx.betweenness_centrality(in_graph)
    betweenness_values = betweenness_centrality_parallel(in_graph)
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


