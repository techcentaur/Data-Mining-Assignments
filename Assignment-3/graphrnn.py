"""
Implement dataloader class
that implements new version of bfs
technqiue as desribed in the paper
"""
from config import config
import queue
import networkx as nx

class GraphRNNLoader:
	"""
	Pytorch Dataloader class but for graphRNNs
	"""

	def __init__(self, graphs):
		self.matrices = [nx.to_numpy_matrix(G) for g in graphs]
		self.num_graphs = len(self.matrices)
		self.trunc_length = self.truncation()


	def __str__(self):
		string = ""
		string += "[*] GraphRNN Loader \n"
		return string

	def __getitem__(self, i):
		"""returns an item according to the equation:
								S_pi = f_S(BFS(G, pi))
		"""
		
		# get the graph at ith index (say worker)
		worker = self.matrices[index].copy()
		workerN = worker.shape[0]

		# choose a random ordering: pi
		pi = np.random.permutation(workerN)
		ordering = np.ix_(pi, pi)
		worker = worker[ordering]
		workerG = nx.from_numpy_matrix(np.asmatrix(worker))

		# draw a bfs sequence and arrange graph
		pi_v1 = np.random.randint(workerN)
		bfs_pi = np.array(breadth_first_search(workerG, pi_v1))
		bfs_ordering = np.ix_(bfs_pi, bfs_pi)
		worker = worker[bfs_ordering]

		seq = convert_to_sequence(worker, workerN)

		return  seq


	def convert_to_sequence(self, graph, num):
	    """ Convert graph to truncated sequence
	    """

	    graph = np.tril(graph, k = -1)[1 : num, 0 : num-1]
	    sequence = np.zeros((num, self.trunc_length))

	    t = self.trunc_length
	    for i in range(num):
	    	p1 = max(i-t+1 , 0)
	    	sequence[i, (p1-(i+1))+t:t] = graph[i, p1:i+1]
	    return sequence

	def get_max_truncation(self, graph, num):
		"""
		Return the max of Ms: which are the BFS-frontier intervals: A_i
		"""

	    graph = np.tril(graph, k = -1)[1 : num, 0 : num-1]

	    Ms = []
	    pointer1 = 0
	    for i in range(num):
	        A_interval = graph[i, pointer1:i+1]
	        pointer1 = (i+1) - len(A_interval) + np.amin(np.nonzero(A_interval)[0])
	        Ms.append(A_interval)
	      
		max_of_Ms = max([len(x) for x in Ms])
	    return max_of_Ms

	def breadth_first_search(self, graph, first_node):
		"""
		Do BFS on the `graph` starting from `first_node`
		"""
		bfs = []
		successors = nx.bfs_successors(graph, first_node)

		q = queue.Queue()
		q.put(first_node)

		while not q.empty():
			pop = q.get()
			bfs.append(pop)

			succ = successors[pop]
			if succ:
				for s in succ:
					q.put(s)

		return bfs


	def truncation(self):
		""" 
		M: To convert S_i_pi into fixed M-dimensional vector
			To find the max dist, so we can truncate the possible edge-predictions
		"""

		fixed_size = []
		for i in range(config["variables"]["truncate_range"]):

			# randomly select a graph: worker
			index = np.random.randint(self.num_graphs)
			worker = self.matrices[index].copy()
			workerN = worker.shape[0]

			# choose a random ordering: pi
			pi = np.random.permutation(workerN)
			ordering = np.ix_(pi, pi)
			worker = worker[ordering]
			workerG = nx.from_numpy_matrix(np.asmatrix(worker))

			# draw a bfs sequence and arrange graph
			pi_v1 = np.random.randint(workerN)
			bfs_pi = np.array(breadth_first_search(workerG, pi_v1))
			bfs_ordering = np.ix_(bfs_pi, bfs_pi)
			worker = worker[bfs_ordering]

			# find max frontier length: M
			fixed_size.append(get_max_truncation(worker, workerN))

		return max(fixed_size)

