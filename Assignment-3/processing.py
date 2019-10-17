import queue
import numpy as np
import networkx as nx
from config import config


class DataProcessor:
	def __init__(self, graphs):
		self.graphs = graphs
		self.maxnodes = max([self.graphs[x].shape[0] for x in range(len(self.graphs))])

		self.num_graphs = len(self.graphs)
		self.trunc_length = self.truncation()

		print("[*] Total number of graphs - {}".format(self.num_graphs))
		print("[*] Max number of nodes - {}".format(self.maxnodes))

	def __str__(self):
		string = ""
		string += "[*] GraphRNN Loader \n"
		return string

	def __len__(self):
		return self.num_graphs

	def __getitem__(self, i):
		worker = self.graphs[i].copy()
		worker_nodes = worker.shape[0]

		pi = np.random.permutation(worker_nodes)
		worker = worker[np.ix_(pi, pi)]

		pi_v1 = np.random.randint(worker_nodes)
		bfs_pi = np.array(self.breadth_first_search(worker, pi_v1))
		worker = worker[np.ix_(bfs_pi, bfs_pi)]

		seq = self.convert_to_sequence(worker, worker_nodes)
		return  {'seq': seq}

	def convert_to_sequence(self, graph, num):
		graph = np.tril(graph, k = -1)[1 : num, 0 : num-1]
		sequence = np.zeros((num, self.trunc_length))

		t = self.trunc_length
		for i in range(num-1):
			p1 = max(i-t+1 , 0)
			sequence[i, (p1-(i+1))+t:t] = graph[i, p1:i+1]
		return sequence

	def get_max_truncation(self, graph, num):
		graph = np.tril(graph, k = -1)[1:num, 0:num-1]

		Ms = []
		pointer1 = 0
		for i in range(num-1):
			A_interval = graph[i, pointer1:i+1]
			pointer1 = (i+1) - len(A_interval) + np.amin(np.nonzero(A_interval)[0])
			Ms.append(A_interval)

		max_of_Ms = max([len(x) for x in Ms])
		return max_of_Ms

	def breadth_first_search(self, graph, first_node):
		bfs = []
		num = graph.shape[0]
		visited = [False for x in range(num)]

		q = queue.Queue()
		q.put(first_node)
		visited[first_node] = True
		while not q.empty():
			pop = q.get()
			bfs.append(pop)

			for succ in range(num):
				if int(graph[pop, succ]) == 1:
					if not visited[succ]:
						q.put(succ)
						visited[succ] = True
		return bfs


	def truncation(self):
		fixed_size = []
		for i in range(config["variables"]["truncate_range"]):
			index = np.random.randint(self.num_graphs)
			worker = self.graphs[index].copy()
			worker_nodes = worker.shape[0]

			pi = np.random.permutation(worker_nodes)
			worker = worker[np.ix_(pi, pi)]

			pi_v1 = np.random.randint(worker_nodes)
			bfs_pi = np.array(self.breadth_first_search(worker, pi_v1))
			worker = worker[np.ix_(bfs_pi, bfs_pi)]

			fixed_size.append(self.get_max_truncation(worker, worker_nodes))

		return max(fixed_size)