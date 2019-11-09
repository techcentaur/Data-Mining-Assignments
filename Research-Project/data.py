import numpy as np
import networkx as nx

from processing import DataGenerator
from config import config

class Data:
    def __init__(self):
        self.labelMap = {}

    def get_graphs(self):
        file = config["data"]["filepath"]
        labelMapIndex = 0

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
                        lab = line.strip('\n')
                        # print(lab)
                        if lab in self.labelMap:
                            nodes_list.append(
                                (nodes_read, {'label': self.labelMap[lab]}))
                        else:
                            self.labelMap[lab] = labelMapIndex
                            labelMapIndex += 1
                            nodes_list.append(
                                (nodes_read, {'label': self.labelMap[lab]}))


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

    def network_graph_to_matrix(self, graphs, e_label_max_length=4, n_label_max_length=5):
        # conversion of graph as object of networkx to numpy adjacency matrix
       
        adj_matrices = [nx.to_numpy_matrix(g) for g in graphs]
        edge_labels, node_labels = [], []

        for i, graph in enumerate(graphs):
            num_nodes = adj_matrices[i].shape[0]

            e_labels = np.zeros((num_nodes, num_nodes, e_label_max_length))
            n_labels = np.zeros((num_nodes, n_label_max_length))

            # one hot encoding for zeros
            for k in range(num_nodes):
                for j in range(num_nodes):
                    e_labels[k, j, 0] = 1
            for k in range(num_nodes):
                n_labels[k, 0] = 1

            for n1, n2, l1 in graph.edges(data=True):
                e_labels[n1, n2, l1['label']] = 1
                e_labels[n1, n2, 0] = 0
                e_labels[n2, n1, l1['label']] = 1
                e_labels[n2, n1, 0] = 0

            edge_labels.append(e_labels)

            for (n1, l1) in graph.nodes(data=True):
                n_labels[n1, l1['label']] = 1
            node_labels.append(n_labels)

        return [adj_matrices, edge_labels, node_labels]


if __name__ == "__main__":
    d = Data()
    graphs = d.get_graphs()
    p = d.network_graph_to_matrix(graphs)
    dg = DataGenerator(p[0], p[1], p[2])


# POSSIBLE CHANGES
"""
Need not make a matrix for edge labels
Can possibly generate edge labels later on 
And leave the edges as 1,3,4 in the adjency matrix itself
"""
