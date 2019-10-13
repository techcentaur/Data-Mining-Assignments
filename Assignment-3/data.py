import numpy as np
from config import config

import networkx as nx


class Data:
	def __init__(self):
		pass

	def get_graphs(self):
		"""
		filepath:
		read from the given graph file path from config.yml

		return:
		a list of all graphs into networkx objects

		one graph object must have:
			- all nodes
			- all node's labels
			- all edges and their labels

		"""

		file = config["data"]["filepath"]
		
		G = nx.Graph()
		graph_data = []
		with open(file, 'r') as f:
			idx = -1
			for line in f:
				if line.startswith("#"):
					idx += 1
					graph_data.append([])
				else:
					graph_data[idx].append(line)


		


		return graphs