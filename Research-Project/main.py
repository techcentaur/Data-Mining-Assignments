from processing import DataGenerator
from data import Data
from models import combined_gru, generate
import sys
import time
import random

NUM_GRAPHS_TO_GENERATE = 50
BATCH_SIZE = 64
EPOCHS = 5
VALIDATION_SPLIT = 0.2

if __name__ == "__main__":
    start = time.time()
    d = Data()
    graphs = d.get_graphs(sys.argv[1])
    num_graphs = len(graphs)
    split_index = round(VALIDATION_SPLIT*num_graphs)
    test_graphs = graphs[:split_index]
    validation_graphs = graphs[split_index:]

    test_p = d.network_graph_to_matrix(test_graphs)
    test_dg = DataGenerator(test_p[0], test_p[1], test_p[2], d.labelMap,
                            d.edge_label_map, batch_size=BATCH_SIZE)

    validation_p = d.network_graph_to_matrix(test_graphs)
    validation_dg = DataGenerator(validation_p[0], validation_p[1], validation_p[2], d.labelMap,
                                  d.edge_label_map, batch_size=BATCH_SIZE)

    model = combined_gru(test_dg)
    model.fit_generator(test_dg, epochs=EPOCHS)
    model.save(sys.argv[3], include_optimizer=True, overwrite=True)
    print('Training finished:', time.time()-start)

    i = 0
    num_empty_graphs_gen_till_now = 0
    with open(sys.argv[2], "a") as gen_file:
        while i < NUM_GRAPHS_TO_GENERATE:
            y = generate(model, test_dg)

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
