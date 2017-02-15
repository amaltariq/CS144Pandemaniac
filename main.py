import json 
import os
import time
import sys
import networkx as nx
import random
import matplotlib.pyplot as pyplot
import numpy as np
import json_parser as jp
import pick_nodes as pn

def get_graph(filename):
    myGraph='TestGraphs/'+filename+'.json'
    data = jp.parser(myGraph)
    G = jp.convert_to_graph(data)
    top_nodes = pn.pick_seeds(G, 5)
    pn.output_nodes(top_nodes, 'testgraph1top.txt')


if __name__ == '__main__':
  get_graph('testgraph1')