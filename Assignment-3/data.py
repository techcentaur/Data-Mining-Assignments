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

        graphs = []
        with open(file, 'r') as f:
            idx = -1
            read_state = 0
            total_nodes = -1
            total_edges = -1
            nodes_read = 0
            edges_read = 0
            nodes_list = []
            edges_list = []
            for line in f:
                if line.startswith("#"):
                    idx += 1
                    G = nx.Graph()
                    graphs.append(G)
                    read_state = 0

                elif read_state == 0:
                    if total_nodes == -1:
                        total_nodes = int(line)
                        nodes_read = 0
                    else:
                        nodes_list.append(
                            (nodes_read, {'label': line.strip('\n')}))
                        # graphs[idx].add_node(
                        #     nodes_read, label=line.strip('\n'))
                        nodes_read += 1
                        if nodes_read == total_nodes:
                            graphs[idx].add_nodes_from(nodes_list)
                            nodes_list = []
                            total_nodes = -1
                            read_state = 1

                elif read_state == 1:
                    if total_edges == -1:
                        total_edges = int(line)
                        edges_read = 0
                    else:
                        edge_params = line.split(' ')
                        edges_list.append((int(edge_params[0]), int(
                            edge_params[1]), {'label': int(edge_params[2])}))
                        # graphs[idx].add_edge(int(edge_params[0]), int(
                        #     edge_params[1]), label=int(edge_params[2]))
                        edges_read += 1
                        if edges_read == total_edges:
                            graphs[idx].add_edges_from(edges_list)
                            edges_list = []
                            total_edges = -1
                            read_state = -1

        return graphs


if __name__ == "__main__":
    d = Data()
    gs = d.get_graphs()
