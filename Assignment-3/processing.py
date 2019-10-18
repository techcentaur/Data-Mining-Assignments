import queue
import numpy as np
import networkx as nx
from numpy.random import (randint, permutation)

from config import config


class DataProcessor:
	def __init__(self, graphs):
		self.graphs = graphs
		
		self.num_graphs = len(self.graphs)
		self.max_nodes = max([self.graphs[x].shape[0] for x in range(len(self.graphs))])

		bigmax = 0
		smolmax = 0
		for i in range(self.num_graphs):
			g = self.graphs[i].copy()

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
		return self.num_graphs

	def __getitem__(self, i):
		g = self.graphs[i].copy()

		pi = permutation(g.shape[0])
		g = g[np.ix_(pi, pi)]

		v = randint(g.shape[0])
		bfs = self.breadth_first_search(g, v)

		g = g[np.ix_(bfs, bfs)]
		g = np.tril(g, k=-1)[1:g.shape[0], 0:g.shape[0]-1]

		seq = np.zeros((g.shape[0], self.M))
		t = self.M

		for j in range(g.shape[0]-1):
			p1 = max(j-t+1, 0)
			seq[j, (p1-(j+1))+t:t] = g[j, p1:j+1]
		
		return  {'seq': seq}


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
