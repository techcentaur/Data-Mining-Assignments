from processing import DataGenerator
from data import Data
from models import combined_gru, generate
import sys

NUM_GRAPHS_TO_GENERATE = 50
BATCH_SIZE = 2
EPOCHS = 10

if __name__ == "__main__":
    d = Data()
    graphs = d.get_graphs(sys.argv[1])
    p = d.network_graph_to_matrix(graphs)
    dg = DataGenerator(p[0], p[1], p[2], d.labelMap, d.edge_label_map, batch_size=BATCH_SIZE)

    model = combined_gru(dg.node_one_hot_vector_size,
                         dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)
    model.fit_generator(dg, epochs=EPOCHS)

    gen_file = open(sys.argv[2], "w")

    for i in range(NUM_GRAPHS_TO_GENERATE):
        y = generate(model, dg.node_one_hot_vector_size,
                     dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)

        outp, nodelist = dg.decode_adj(y)
        # print("final")
        # print(outp, nodelist)
        if nodelist.shape[0] != 0:
            dg.write_graph(gen_file, outp, nodelist, i)
        else:
            i -= 1

    gen_file.close()
