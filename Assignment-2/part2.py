import subprocess
import numpy as np

def get_no_of_graphs(filename):
	c = 0
	with open(filename, 'r') as file:
		for line in file:
			if c==5:
				return int(line.split()[-1])
			else:
				if c==5:
					break
				else:
					c+=1
					continue
	return 0

def get_no_of_fpatterns(filename):
	a = subprocess.check_output(['tail', '-5', filename])
	n = int(((a.decode("utf-8")).split("\n")[0]).split()[-1])
	return n

if __name__ == '__main__':
	cmd = "./pafi-1.0.1/Linux/fsg -s 80.0 -t ./Yeast/pafi_smol.txt_graph"
	subprocess.call(cmd.split())

	# n_graphs = get_no_of_graphs("./Yeast/pafi_smol.fp")
	n_graphs = 100
	# n_fpatterns = get_no_of_fpatterns("./Yeast/pafi_smol.fp")
	n_fpatterns = 20

	print("patterns", n_fpatterns)
	print("graphs", n_graphs)

	fvectors = np.zeros((n_graphs, n_fpatterns))

	with open("./Yeast/pafi_smol.tid", 'r') as file:
		fv = 0
		for line in file:
			vals = line.split()
			# print(vals[0])
			for i in range(1, len(vals)):
				fvectors[int(vals[i])][fv] = 1
			fv+=1

	print(fvectors)


	# 1. For a query graph q, read the file, "./Yeash/pafi_smol.fp" and see which are the frequent-graph
	# are a subgraph of q -> make a feature vector for q 
	# 2. Search in fvectors and see which are the graphs (indices) which contains the feature vector for q
	# Do this till

