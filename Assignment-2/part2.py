import subprocess
import numpy as np
import graph_tool.all as gt
import pafi


def get_no_of_graphs(filename):
    c = 0
    with open(filename, 'r') as file:
        for line in file:
            if c == 5:
                return int(line.split()[-1])
            else:
                if c == 5:
                    break
                else:
                    c += 1
                    continue
    return 0


def get_no_of_fpatterns(filename):
    a = subprocess.check_output(['tail', '-5', filename])
    n = int(((a.decode("utf-8")).split("\n")[0]).split()[-1])
    return n

# input: frequent pattern (fp) filename/path that contains frequent subgraphs
# output: list of Graph DS (Graphs corresponding to frequent subgraphs)


def get_freq_sub_graph(filename):
    # g = Graph(directed=)
    freq_sg_file = open(filename, "r")

	for _ in range(25):
		line = freq_sg_file.readline()

	# numpy array?
	freq_sg_list = []

	g = None
	for line in freq_sg_file:
		splited = line.split(' ')
		if splited[0] == 't':
			if g is not None:
				freq_sg_list.append(g)
			g = gt.Graph(directed=False)
			g.vertex_properties["molecule"] = g.new_vertex_property("string")
			g.edge_properties["bond"] = g.new_edge_property("int")
		elif splited[0] == 'v':
			v = g.add_vertex()
			g.vertex_properties["molecule"][v] = splited[2]
		elif splited[0] == 'u':
			e = g.add_edge(
			g.vertex(int(splited[1])), g.vertex(int(splited[2])))
			g.vertex_properties["bond"][e] = int(splited[3])

	return freq_sg_list

# similar to get_freq_sub_graph, read query graphs converts the to Graph DS saves them in a list


def get_query_graphs(filename):
	outfilepath = pafi.change_format(
	    filename, outfile="./something", verbose=False)
	qg_file = open(outfilepath, "r")

	# numpy array?
	qg_list = []

	g = None
    for line in freq_sg_file:
        if splited[0] == 't':
            if g is not None:
                qg_list.append(g)
            g = gt.Graph(directed=False)
            g.vertex_properties["molecule"] = g.new_vertex_property("string")
            g.edge_properties["bond"] = g.new_edge_property("int")
        elif splited[0] == 'v':
            v = g.add_vertex()
            g.vertex_properties["molecule"][v] = splited[2]
        elif splited[0] == 'u':
            e = g.add_edge(
                g.vertex(int(splited[1])), g.vertex(int(splited[2])))
            g.vertex_properties["bond"][e] = int(splited[3])

        return qg_list

# makes feature vectors for query graphs
# input: q_gs = query graph list, f_sgs = frequent subgraphs list
# output: 2d array i th row contains feature vector of ith query graph
def index_query_graphs(q_gs, f_sgs):
	fvectors = np.zeros((len(q_gs), len(f_sgs)))
	fv = 0
	for f_sg in f_sgs:
		qv = 0
		for q_g in q_gs:
			vl = np.concatenate(f_sg.vertex_properties["molecule"].get_array(), q_g.vertex_properties["molecule"].get_array())
        	el = np.concatenate(f_sg.vertex_properties["bond"].get_array(), q_g.vertex_properties["bond"].get_array())
			# subgraph isomorphisms return list of maps, i.e we check for empty if not a subgraph
			# check subgraph parameter in function below 
			if len(graph_tool.topology.subgraph_isomorphism(
            	sub, g, max_n=1, vertex_label=vl, edge_label=vl, induced=True, subgraph=False, generator=False)) > 0:
				fvectors[qv][fv] = 1
			qv += 1
		fv += 1

	return fvectors


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
            fv += 1

    print(fvectors)

    # 1. For a query graph q, read the file, "./Yeash/pafi_smol.fp" and see which are the frequent-graph
    # are a subgraph of q -> make a feature vector for q
    # 2. Search in fvectors and see which are the graphs (indices) which contains the feature vector for q
    # Do this till
