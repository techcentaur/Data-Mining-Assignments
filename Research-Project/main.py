from processing import DataGenerator
from data import Data
from models import combined_gru, generate
import sys
import time

# NUM_GRAPHS_TO_GENERATE = 1000
BATCH_SIZE = 64
EPOCHS = 20

if __name__ == "__main__":
    start = time.time()
    d = Data()
    graphs = d.get_graphs(sys.argv[1])
    NUM_GRAPHS_TO_GENERATE = len(graphs)
    p = d.network_graph_to_matrix(graphs)
    dg = DataGenerator(p[0], p[1], p[2], d.labelMap,
                       d.edge_label_map, batch_size=BATCH_SIZE)

    model = combined_gru(dg)
    model.fit_generator(dg, epochs=EPOCHS)
    # model.save(sys.argv[3], include_optimizer=True, overwrite=True)
    model.save_weights(sys.argv[3], overwrite=True)
    print('Training finished:', time.time()-start)

    i = 0
    num_empty_graphs_gen_till_now = 0
    total_write_time = 0.0
    with open(sys.argv[2], 'w') as gen_file:
        while i < NUM_GRAPHS_TO_GENERATE:
            start = time.time()
            ys = generate(model, dg, batch_size=BATCH_SIZE)
            for y in ys:
                if not (i < NUM_GRAPHS_TO_GENERATE):
                    break
                outp, nodelist = dg.decode_adj(y)
                print('Generated graph:', time.time() - start)
                if nodelist.shape[0] != 0:
                    b = dg.write_graph(gen_file, outp, nodelist, i)
                    gen_file.flush()
                    if b:
                        print("graph #" + str(i) + " written")
                        i += 1
                    else:
                        num_empty_graphs_gen_till_now += 1
                        print("Bad graph #"+str(num_empty_graphs_gen_till_now) +
                              " generated, skipping from writing")
                else:
                    num_empty_graphs_gen_till_now += 1
                    print("Bad graph #"+str(num_empty_graphs_gen_till_now) +
                          " generated, skipping from writing")
            this_iter_time = time.time()-start
            print('Graphs writing till: ', str(i), ' time: ', this_iter_time)
            total_write_time += this_iter_time
        print('Total writing time: ', total_write_time)
