import json
from pprint import pprint
import networkx as nx

def parser(file_name):
	with open(file_name) as data_file:
		data = json.load(data_file)

	return data

def convert_to_graph(adj_lst):
	G = nx.from_dict_of_lists(adj_lst)
	return G