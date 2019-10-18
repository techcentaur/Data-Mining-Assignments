import numpy as np
import networkx as nx

from config import config

class Data:
    def __init__(self):
        self.labelMap = {}
        self.edge_encoding = {}

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

                        if int(edge_params[2]) not in self.edge_encoding:
                            self.edge_encoding[int(edge_params[2])] = True
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

        matrices = [nx.to_numpy_matrix(g) for g in graphs]
        return matrices

    def network_graph_to_matrix(self, graph, is_list=False):        
        if is_list:
            alist = []
            for g in graph:
                d = dict(g.nodes(data=True))            
                a = np.zeros((len(d), len(d), 1+len(self.edge_encoding)))

                for x, y, d in list(g.edges(data=True)):
                    a[x][y][0] = 1
                    a[x][y][d['label']] = 1

                    a[y][x][0] = 1
                    a[y][x][d['label']] = 1

                alist.append(a)
            return alist

        else:
            d = dict(graph.nodes(data=True))            
            a = np.zeros((len(d), len(d), 1+len(self.edge_encoding)))

            for x, y, d in list(graph.edges(data=True)):
                a[x][y][0] = 1
                a[x][y][d['label']] = 1

                a[y][x][0] = 1
                a[y][x][d['label']] = 1

            return a

if __name__ == "__main__":
    d = Data()
    gs = d.get_graphs()

    graphs = d.network_graph_to_matrix(gs, is_list=True)
