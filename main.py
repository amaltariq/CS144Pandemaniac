import json_parser as jp
import pick_nodes as pn
import time

if __name__ == '__main__':
    start = time.time()
    file_name = 'Day2Graphs/8.35.2.json'

    file_name_str = file_name.split('.')
    num_seeds = int(file_name_str[1])

    data = jp.parser(file_name)
    G = jp.convert_to_graph(data)

    top_nodes = pn.pick_seeds(G, num_seeds)
    pn.output_nodes(top_nodes, ''.join(file_name_str[0:3]))

    end = time.time()
    print('Runtime ' + str(end - start))