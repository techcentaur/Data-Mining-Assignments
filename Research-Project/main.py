from processing import DataGenerator
from data import Data
from models import combined_gru, generate
import sys
import time
import random

NUM_GRAPHS_TO_GENERATE = 50
BATCH_SIZE = 64
EPOCHS = 5

if __name__ == "__main__":
    start = time.time()
    d = Data()
    graphs = d.get_graphs(sys.argv[1])
    num_graphs = len(graphs)
    test_graphs = graphs[:split_index]
    validation_graphs = graphs[split_index:]

    p = d.network_graph_to_matrix(test_graphs)
    dg = DataGenerator(p[0], p[1], p[2], d.labelMap,
                       d.edge_label_map, batch_size=BATCH_SIZE)

    model = combined_gru(dg)
    model.fit_generator(dg, epochs=EPOCHS)
    model.save(sys.argv[3], include_optimizer=True, overwrite=True)
    print('Training finished:', time.time()-start)

    i = 0
    num_empty_graphs_gen_till_now = 0
    with open(sys.argv[2], "a") as gen_file:
        while i < NUM_GRAPHS_TO_GENERATE:
            y = generate(model, dg)

            outp, nodelist = dg.decode_adj(y)
            print('Generated graph:', time.time() - start)
            if nodelist.shape[0] != 0:
                dg.write_graph(gen_file, outp, nodelist, i)
                print("graph #" + str(i) + " written")
                i += 1
                gen_file.flush()
            else:
                num_empty_graphs_gen_till_now += 1
                print("Empty graph #"+str(num_empty_graphs_gen_till_now) +
                      " generated, skipping from writing")
