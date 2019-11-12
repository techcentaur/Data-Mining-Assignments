import queue

import keras
import numpy as np
from numpy.random import (randint, permutation)


class DataGenerator(keras.utils.Sequence):

    def __init__(self, g_matrices, e_labels, n_labels, n_label_map, e_label_map, batch_size=64):
        self.g_matrices = g_matrices
        self.e_labels = e_labels
        self.n_labels = n_labels

        self.n_label_inv_map = {v: k for k, v in n_label_map.items()}
        self.e_label_inv_map = {v: k for k, v in e_label_map.items()}

        self.num_graphs = len(g_matrices)
        self.max_nodes = max([g_matrices[x].shape[0] for x in range(len(g_matrices))]) + 1

        self.edge_one_hot_vector_size = e_labels[0].shape[2]
        self.node_one_hot_vector_size = n_labels[0].shape[1]

        self.batch_size = batch_size

        bigmax = 0
        smolmax = 0

        for i in range(self.num_graphs):
            g = self.g_matrices[i].copy()

            pi = permutation(g.shape[0])
            g = g[np.ix_(pi, pi)]

            v = randint(g.shape[0])
            bfs = self.breadth_first_search(g, v)

            g = g[np.ix_(bfs, bfs)]
            g = np.tril(g, k=-1)[1:g.shape[0], 0:g.shape[0] - 1]

            k = 0
            for j in range(g.shape[0] - 1):
                f = g[j, k:j + 1]
                k = (j + 1) - len(f) + np.amin(np.nonzero(f)[0])

                if len(f) > smolmax:
                    smolmax = len(f)

            if smolmax > bigmax:
                bigmax = smolmax

        self.M = bigmax

    def __len__(self):
        return self.num_graphs // self.batch_size

    def __getitem__(self, batch_index):

        seqshape = self.M * self.edge_one_hot_vector_size + self.node_one_hot_vector_size
        n1h = self.node_one_hot_vector_size
        e1h = self.edge_one_hot_vector_size

        # print("Seqshape: ", seqshape)
        # print("MAX NODES: ", self.max_nodes)
        # print(self.M, e1h, n1h)

        X = np.zeros((self.batch_size, self.max_nodes, seqshape))
        Y = np.zeros((self.batch_size, self.max_nodes, seqshape))

        SOS = np.zeros((1, seqshape))
        EOS = np.zeros((1, seqshape))

        SOS[0, 0] = 1
        EOS[0, 1] = 1
        for i in range(self.M):
            SOS[0, n1h + i * e1h] = 1
            EOS[0, n1h + i * e1h] = 1

        self.SOS = SOS

        for enum, g in enumerate(
                self.g_matrices[self.batch_size * batch_index: self.batch_size * (batch_index + 1)]):

            g = g.copy()
            e = self.e_labels[enum + self.batch_size * batch_index].copy()
            n = self.n_labels[enum + self.batch_size * batch_index].copy()

            pi = permutation(g.shape[0])

            g = g[np.ix_(pi, pi)]
            e = e[np.ix_(pi, pi)]
            n = n[np.ix_(pi)]

            v = randint(g.shape[0])
            bfs = self.breadth_first_search(g, v)

            g = g[np.ix_(bfs, bfs)]
            e = e[np.ix_(bfs, bfs)]
            n = n[np.ix_(bfs)]

            g = np.tril(g, k=-1)[1:g.shape[0], 0:g.shape[0] - 1]

            t = self.M
            seq = np.zeros((g.shape[0], seqshape))

            for j in range(g.shape[0] - 1):
                p1 = max(j - t + 1, 0)
                for k in range(p1, j + 1):
                    seq[j, e1h * (k - (j + 1) + t) + n1h: e1h * (k - (j + 1) + t + 1) + n1h] = e[j, k, 0:t]
                seq[j, 0:n1h] = n[j, 0:n1h]

            X[enum, 1: seq.shape[0], :] = seq[0:seq.shape[0] - 1, :]
            Y[enum, 0: seq.shape[0], :] = seq

            X[enum, 0] = SOS
            Y[enum, g.shape[0]] = EOS
            X[enum, g.shape[0] + 1] = EOS

            # Y:
            # seq
            # EOS -> 0100 100 100
            # 0000000000000000

            # X:
            # SOS -> 1000 100 100
            # seq
            # EOS -> 0100 100 100
        # print("X",  X, end='\n\n\n\n')
        # print("Y",  Y)
        return X, Y

    def on_epoch_end(self):
        # may want to implement
        pass

    def breadth_first_search(self, g, v):
        bfs = []
        num = g.shape[0]
        visited = [False for x in range(num)]

        q = queue.Queue()
        q.put(v)
        visited[v] = True

        while not q.empty():
            pop = q.get()
            bfs.append(pop)

            for succ in range(num):
                if int(g[pop, succ]) == 1:
                    if not visited[succ]:
                        q.put(succ)
                        visited[succ] = True

        return np.array(bfs)

    def decode_adj(self, long_adj):
        '''
            recover to adj from adj_output
            note: here adj_output have shape (n-1)*m
        '''

        long_adj = long_adj[1:]

        adj_output = np.zeros((long_adj.shape[0], self.M))
        node_list = np.zeros((long_adj.shape[0],))

        for i in range(long_adj.shape[0]):
            node_list[i] = np.argmax(long_adj[i, 0:self.node_one_hot_vector_size])
            for j in range(self.M):
                adj_output[i, j] = np.argmax(long_adj[i,
                                             self.node_one_hot_vector_size + self.edge_one_hot_vector_size * j: self.node_one_hot_vector_size + self.edge_one_hot_vector_size * (
                                                     j + 1)])

        max_prev_node = self.M
        adj = np.zeros((adj_output.shape[0], adj_output.shape[0]))
        for i in range(adj_output.shape[0]):
            input_start = max(0, i - max_prev_node + 1)
            input_end = i + 1
            output_start = max_prev_node + max(0, i - max_prev_node + 1) - (i + 1)
            output_end = max_prev_node
            adj[i, input_start:input_end] = adj_output[i, ::-1][output_start:output_end]  # reverse order
        adj_full = np.zeros((adj_output.shape[0] + 1, adj_output.shape[0] + 1))
        n = adj_full.shape[0]
        adj_full[1:n, 0:n - 1] = np.tril(adj, 0)
        adj_full = adj_full + adj_full.T

        count = 0
        for nl in node_list:
            if nl == 1 or nl == 0:
                break
            count += 1

        return adj_full[:count, :count], node_list[:count]

    def write_graph(self, file, adj_list, node_list, graph_id):
        output_string = ""
        output_string += "# " + str(graph_id) + "\n"
        output_string += str(node_list.shape[0]) + "\n"
        # write nodes
        for node in node_list:
            # considering SOS doesn't occur in between graph
            output_string += str(self.n_label_inv_map[node]) + "\n"

        num_edges = 0
        edge_string = ""
        # write edges
        for i in range(adj_list.shape[0]):
            for j in range(0, i):
                label = adj_list[i][j]
                if label != 0:
                    edge_string += str(i) + " " + str(j) + " " + str(self.e_label_inv_map[label]) + "\n"
                    num_edges += 1

        if num_edges != 0:
            output_string += str(num_edges) + "\n" + edge_string + "\n"
        else:
            output_string += str(num_edges) + "\n"

        file.write(output_string)
