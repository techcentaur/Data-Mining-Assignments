from keras.layers import GRU, Activation, Input, Reshape, Concatenate, Lambda
from keras import Model
import keras
import functools
import operator
import numpy as np
from processing import DataGenerator
from  data import Data


DROPOUT_RATE = 0.5
NODES_LAYERS_DMS = (2, 4)
EDGES_LAYERS_DMS = (2, 4)
COMBINED_LAYERS_DMS = (2, 4)


# Input is expected to be flattened concatenated Node Label ohv and edge labels' adjacency list ohv
# In the vocabulary of node labels, the first token is SOS, second is EOS.
# In the vocabulary of edge labels, the first token is NO_EDGE.
def combined_gru(node_vocab_size, edge_vocab_size, max_nodes, trunc_length, layers_dms=COMBINED_LAYERS_DMS, dropout_rate=DROPOUT_RATE):
    input_shape = (max_nodes, node_vocab_size + edge_vocab_size*trunc_length)
    x = Input(input_shape)
    y = x
    for dm in layers_dms:
        y = GRU(dm, activation='tanh', dropout=dropout_rate,
                recurrent_dropout=dropout_rate, return_sequences=True)(y)
    y = GRU(input_shape[1], dropout=dropout_rate, recurrent_dropout=dropout_rate, return_sequences=True)(y)

    node_softmax = Lambda(lambda x: x[:, :, :node_vocab_size])(y)
    edge_softmax = Lambda(lambda x: x[:, :,  node_vocab_size:])(y)

    edge_softmax = Reshape((max_nodes, trunc_length, edge_vocab_size))(edge_softmax)

    node_softmax = Activation('softmax')(node_softmax)
    edge_softmax = Activation(lambda x: keras.activations.softmax(x, -1))(edge_softmax)

    edge_softmax = Reshape((max_nodes, trunc_length*edge_vocab_size,))(edge_softmax)
    y = Concatenate()([node_softmax, edge_softmax])

    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='Adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    return model


def node_gru(input_shape, layers_dms=NODES_LAYERS_DMS, dropout_rate=DROPOUT_RATE):
    x = Input(input_shape)
    y = x
    for dm in layers_dms:
        y = GRU(dm, activation='tanh', dropout=dropout_rate,
                recurrent_dropout=dropout_rate, return_sequences=True)(y)
    y = GRU(input_shape[1], activation=lambda x: keras.activations.softmax(x, 1), dropout=dropout_rate,
            recurrent_dropout=dropout_rate, return_sequences=True)(y)
    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='Adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    return model


def edge_gru(input_shape, layers_dms=EDGES_LAYERS_DMS, dropout_rate=DROPOUT_RATE):
    x = Input(input_shape)
    # size = functools.reduce(operator.mul, input_shape, 1)
    input_shape_list = list(input_shape)
    y = Reshape(tuple(
        input_shape_list[:2]+[input_shape_list[-2]*input_shape_list[-1]]), name='predictions')(x)
    for dm in layers_dms:
        y = GRU(dm, activation='tanh', dropout=dropout_rate,
                recurrent_dropout=dropout_rate, return_sequences=True)(y)
    # size = flattened version of the output shape
    # size = functools.reduce(operator.mul, input_shape, 1)
    # print(size)
    # print(input_shape)
    y = GRU(input_shape_list[-1]*input_shape_list[-2], activation='tanh', dropout=dropout_rate,
            recurrent_dropout=dropout_rate, return_sequences=True)(y)
    model = Model(inputs=x, outputs=y)
    model.summary()
    y = Reshape(input_shape, name='predictions')(y)
    y = keras.activations.softmax(y, axis=1)

    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='Adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    return model

def sample(adj_mat_row, node_vocab_size, edge_vocab_size, max_nodes, trunc_length):
    node_part = adj_mat_row[:node_vocab_size]
    edge_part = adj_mat_row[node_vocab_size:]
    edge_part = np.reshape(edge_part, (trunc_length, edge_vocab_size))

    out_node_part = np.zeros((node_vocab_size,))
    a = np.random.choice(node_vocab_size, 1, node_part.tolist())
    out_node_part[a] = 1

    out_edge_part = np.zeros((trunc_length, edge_vocab_size))
    for i in range(trunc_length):
        print()
        out_edge_part[i, int(np.random.choice(edge_vocab_size, 1, edge_part[i].tolist())[0])] = 1

    out_edge_part = np.reshape(out_edge_part, (trunc_length * edge_vocab_size,))
    return np.concatenate((out_node_part, out_edge_part))



def generate(model, node_vocab_size, edge_vocab_size, max_nodes, trunc_length):
    # init starting graph input
    nodes_input = np.zeros(node_vocab_size)
    # SOS
    nodes_input[0] = 1
    edges_input = np.zeros((trunc_length, edge_vocab_size))
    # NO_EDGE
    edges_input[:, 0] = 1
    edges_input = np.reshape(edges_input, (trunc_length * edge_vocab_size,))
    combined_input = np.concatenate((nodes_input, edges_input))
    X = np.zeros((1, max_nodes, node_vocab_size + edge_vocab_size*trunc_length))
    X[0, 0, :] = combined_input

    for i in range(max_nodes-1):
        y = model.predict((X))[0]
        y = sample(y[i, :], node_vocab_size, edge_vocab_size, max_nodes, trunc_length)
        X[0, i + 1, :] = y
        if y[1] == 1:
            break

    return X


import sys
d = Data()
graphs = d.get_graphs()
p = d.network_graph_to_matrix(graphs)

print("Sizes: ")
print(d.n_hot_vector)
print(d.e_hot_vector)

print("Label Map:")
print(d.labelMap)
print(d.edge_label_map)

print("Graph:")
for g in graphs:
    print(g.edges(data=True))
    print(g.nodes(data=True))

dg = DataGenerator(p[0], p[1], p[2], batch_size=2)
model = combined_gru(dg.node_one_hot_vector_size, dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)
# model = combined_gru = 
# model.fit(np.random.rand(32, 5, 10 + 4*3), np.random.rand(32, 5, 10 + 4*3), batch_size=8)
model.fit_generator(dg)
y = generate(model, dg.node_one_hot_vector_size, dg.edge_one_hot_vector_size,  dg.max_nodes,  dg.M)
print(y.shape)
print(y)
