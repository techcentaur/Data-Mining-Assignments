import subprocess
import numpy as np
import graph_tool.all as gt
import pafi
import json
import ast
import sys
import os



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
    freq_sg_file = open(filename, "r")

    for _ in range(24):
        line = freq_sg_file.readline()

    freq_sg_list = []

    g = None
    for line in freq_sg_file:
        splited = line.split()
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
            g.edge_properties["bond"][e] = int(splited[3])

    freq_sg_list.append(g)
    return freq_sg_list


# similar to get_freq_sub_graph, read query graphs converts the to Graph DS saves them in a list
def get_query_graphs(filename):
    outfile, mapping = pafi.change_format(filename)
    qg_file = open(outfile, "r")

    qg_list = []

    g = None
    for line in qg_file:
        splited = line.split()

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
            g.edge_properties["bond"][e] = int(splited[3])

    qg_list.append(g)
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
            # subgraph isomorphisms return list of maps, i.e we check for empty if not a subgraph
            # check subgraph parameter in function below 
            if len(gt.subgraph_isomorphism(
                f_sg, q_g, max_n=1, vertex_label=(f_sg.vertex_properties["molecule"], q_g.vertex_properties["molecule"]), 
                edge_label= (f_sg.edge_properties["bond"], q_g.edge_properties["bond"]), induced=False, subgraph=True, generator=False)) > 0:
                fvectors[qv][fv] = 1
            qv += 1
        fv += 1
    return fvectors


def get_database_graph_objects(filename):
    qg_file = open(filename, "r")
    qg_list = []

    g = None
    for line in qg_file:
        splited = line.split()
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
            g.edge_properties["bond"][e] = int(splited[3])

    qg_list.append(g)
    return qg_list


def get_map(filepath):
    fp = open(filepath, 'r')
    out = json.load(fp)
    return out


if __name__ == '__main__':
    transaction_database = sys.argv[1]
    support = 72.0

    outfile, mapfile = pafi.change_format(transaction_database)
    FNULL = open(os.devnull, 'w')
    command = ['./pafi-1.0.1/Linux/fsg', '-s', str(support), '-t', outfile]
    subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

    root_file = outfile.split('/')[-1].split('.')[0]
    n_graphs = get_no_of_graphs(root_file + '.fp')
    n_fpatterns = get_no_of_fpatterns(root_file + '.fp')

    fvectors = np.zeros((n_graphs, n_fpatterns))

    with open(root_file + '.tid', 'r') as file:
        fv = 0
        for line in file:
            vals = line.split()
            for i in range(1, len(vals)):
                fvectors[int(vals[i])][fv] = 1
            fv += 1
        
    print('Indexing complete', flush=True)
    inp = input().split()
    query, output_filename = inp[0], inp[1]

    qgs = get_query_graphs(query)
    fgs = get_freq_sub_graph(root_file + '.fp')
    query_fvectors = index_query_graphs(qgs, fgs)

    database_graphs = get_database_graph_objects(outfile)
    mapping = get_map(mapfile)

    result = {}
    for i in range(query_fvectors.shape[0]):
        result[i] = []
        for j in range(fvectors.shape[0]):
            if (np.all(query_fvectors[i]==np.logical_and(fvectors[j], query_fvectors[i]))):
                x=gt.subgraph_isomorphism(
                qgs[i], database_graphs[j], max_n=1, vertex_label=(qgs[i].vertex_properties['molecule'], database_graphs[j].vertex_properties['molecule']), 
                edge_label= (qgs[i].edge_properties['bond'], database_graphs[j].edge_properties['bond']), induced=False, subgraph=True, generator=False)

                result[i].append(str(mapping[str(j)]))
    
    qs = len(result)
    with open(output_filename, 'w') as f:
        for i in range(qs):
            f.write('\t'.join(result[i]) + '\n')
