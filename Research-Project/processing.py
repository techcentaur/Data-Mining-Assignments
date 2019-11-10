import queue
import numpy as np
import networkx as nx
from config import config
import keras
from numpy.random import (randint, permutation)

class DataGenerator(keras.utils.Sequence):
    def __init__(self, g_matrices, e_labels,  n_labels, batch_size=1):
        self.g_matrices = g_matrices
        self.e_labels = e_labels
        self.n_labels = n_labels
        
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
            g = np.tril(g, k=-1)[1:g.shape[0], 0:g.shape[0]-1]

            k = 0
            for j in range(g.shape[0]-1):
                f = g[j, k:j+1]
                k = (j+1) - len(f) + np.amin(np.nonzero(f)[0])
                
                if len(f) > smolmax:
                    smolmax = len(f)

            if smolmax > bigmax:
                bigmax = smolmax

        self.M = bigmax 

    def __len__(self):
        return (self.num_graphs//self.batch_size)

    def __getitem__(self, batch_index):

        seqshape = self.M*self.edge_one_hot_vector_size + self.node_one_hot_vector_size
        n1h = self.node_one_hot_vector_size
        e1h = self.edge_one_hot_vector_size     
        
        print("Seqshape: ", seqshape)
        print("MAX NODES: ", self.max_nodes)
        print(self.M, e1h, n1h)

        X =  np.zeros((self.batch_size, self.max_nodes, seqshape))
        Y =  np.zeros((self.batch_size, self.max_nodes, seqshape))

        SOS = np.zeros((1, seqshape))
        EOS = np.zeros((1, seqshape))
        
        SOS[0, 0] = 1
        EOS[0, 1] = 1
        for i in range(self.M):
            SOS[0, n1h + i * e1h] = 1
            EOS[0, n1h + i * e1h] = 1


        for enum, g in enumerate(self.g_matrices[self.batch_size *  batch_index: self.batch_size * (batch_index+1) +1]):

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

            g = np.tril(g, k=-1)[1:g.shape[0], 0:g.shape[0]-1]

            t = self.M
            seq = np.zeros((g.shape[0], seqshape))

            for j in range(g.shape[0]-1):
                p1 = max(j-t+1, 0)
                for k in range(p1, j+1):
                    seq[j, e1h*(k-(j+1)+t)+n1h: e1h*(k-(j+1)+t+1)+n1h] = e[j, k,0:t]
                seq[j, 0:n1h] = n[j, 0:n1h]

            X[enum, 1: seq.shape[0], :] = seq[0:seq.shape[0]-1, :]
            Y[enum, 0: seq.shape[0], :] = seq

            X[enum, 0] = SOS
            Y[enum, g.shape[0]] = EOS
            X[enum, g.shape[0]+1] = EOS
        
            # Y:
            # seq
            # EOS -> 0100 100 100
            # 0000000000000000

            # X:
            # SOS -> 1000 100 100
            # seq
            # EOS -> 0100 100 100
        print("X",  X, end='\n\n\n\n')
        print("Y",  Y)
        return  X, Y


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
