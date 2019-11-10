from processing import DataGenerator
from data import Data
from models import combined_gru, generate

NUM_GRAPHS_TO_GENERATE = 100
BATCH_SIZE = 64
EPOCHS = 10

if __name__ == "__main__":
    d = Data()
    graphs = d.get_graphs()
    p = d.network_graph_to_matrix(graphs)
    dg = DataGenerator(p[0], p[1], p[2], batch_size=BATCH_SIZE)

    model = combined_gru(dg.node_one_hot_vector_size,
                         dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)
    model.fit_generator(dg, epochs=EPOCHS)
    for i in range(NUM_GRAPHS_TO_GENERATE):
        y = generate(model, dg.node_one_hot_vector_size,
                     dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)
