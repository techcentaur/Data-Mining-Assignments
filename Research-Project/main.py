from processing import DataGenerator
from data import Data
from models import combined_gru, generate
import sys
import time

NUM_GRAPHS_TO_GENERATE = 50
BATCH_SIZE = 64
EPOCHS = 1

if __name__ == "__main__":
    start = time.time()
    d = Data()
    graphs = d.get_graphs(sys.argv[1])

    p = d.network_graph_to_matrix(graphs)
    dg = DataGenerator(p[0], p[1], p[2], d.labelMap, d.edge_label_map, batch_size=BATCH_SIZE)

    model = combined_gru(dg.node_one_hot_vector_size,
                         dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)
    model.fit_generator(dg, epochs=EPOCHS)
    model.save(sys.argv[3], include_optimizer=True, overwrite=True)
    print('Training finished:', time.time()-start)

    i = 0

    with open(sys.argv[2], "w") as gen_file:
        while i < NUM_GRAPHS_TO_GENERATE:
            y = generate(model, dg.node_one_hot_vector_size,
                         dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)

            outp, nodelist = dg.decode_adj(y)
            print('Generated graph:', time.time() - start)
            if nodelist.shape[0] != 0:
                dg.write_graph(gen_file, outp, nodelist, i)
                i += 1
