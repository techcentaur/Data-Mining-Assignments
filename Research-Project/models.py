from keras.layers import GRU, Activation, Input, Reshape, Concatenate, Lambda, Dropout
from keras import Model
import keras
import functools
import operator
import numpy as np
from processing import DataGenerator
from data import Data


DROPOUT_RATE = 0.3
# NODES_LAYERS_DMS = (100, 100)
# EDGES_LAYERS_DMS = (100, 100)
COMBINED_LAYERS_DMS = (100, 50)


# Input is expected to be flattened concatenated Node Label ohv and edge labels' adjacency list ohv
# In the vocabulary of node labels, the first token is SOS, second is EOS.
# In the vocabulary of edge labels, the first token is NO_EDGE.
# d is datagen for graphs
def combined_gru(d, layers_dms=COMBINED_LAYERS_DMS, dropout_rate=DROPOUT_RATE):
    input_shape = (d.max_nodes, d.node_one_hot_vector_size +
                   d.edge_one_hot_vector_size*d.M)
    x = Input(input_shape)
    y = x
    for dm in layers_dms:
        y = GRU(dm, activation='tanh', dropout=dropout_rate,
                recurrent_dropout=dropout_rate, return_sequences=True)(y)
        y = Dropout(dropout_rate)(y)
    y = GRU(input_shape[1], dropout=dropout_rate,
            recurrent_dropout=dropout_rate, return_sequences=True)(y)

    node_softmax = Lambda(lambda x: x[:, :, :d.node_one_hot_vector_size])(y)
    edge_softmax = Lambda(lambda x: x[:, :,  d.node_one_hot_vector_size:])(y)

    edge_softmax = Reshape(
        (d.max_nodes, d.M, d.edge_one_hot_vector_size))(edge_softmax)

    node_softmax = Activation('softmax')(node_softmax)
    edge_softmax = Activation(
        lambda x: keras.activations.softmax(x, -1))(edge_softmax)

    edge_softmax = Reshape(
        (d.max_nodes, d.M*d.edge_one_hot_vector_size,))(edge_softmax)
    y = Concatenate()([node_softmax, edge_softmax])

    model = Model(inputs=x, outputs=y)
    model.compile(optimizer='Adam', loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    return model


# def node_gru(input_shape, layers_dms=NODES_LAYERS_DMS, dropout_rate=DROPOUT_RATE):
#     x = Input(input_shape)
#     y = x
#     for dm in layers_dms:
#         y = GRU(dm, activation='tanh', dropout=dropout_rate,
#                 recurrent_dropout=dropout_rate, return_sequences=True)(y)
#     y = GRU(input_shape[1], activation=lambda x: keras.activations.softmax(x, 1), dropout=dropout_rate,
#             recurrent_dropout=dropout_rate, return_sequences=True)(y)
#     model = Model(inputs=x, outputs=y)
#     model.compile(optimizer='Adam', loss='binary_crossentropy',
#                   metrics=['accuracy'])
#     model.summary()
#     return model
#
#
# def edge_gru(input_shape, layers_dms=EDGES_LAYERS_DMS, dropout_rate=DROPOUT_RATE):
#     x = Input(input_shape)
#     # size = functools.reduce(operator.mul, input_shape, 1)
#     input_shape_list = list(input_shape)
#     y = Reshape(tuple(
#         input_shape_list[:2]+[input_shape_list[-2]*input_shape_list[-1]]), name='predictions')(x)
#     for dm in layers_dms:
#         y = GRU(dm, activation='tanh', dropout=dropout_rate,
#                 recurrent_dropout=dropout_rate, return_sequences=True)(y)
#     # size = flattened version of the output shape
#     # size = functools.reduce(operator.mul, input_shape, 1)
#     # print(size)
#     # print(input_shape)
#     y = GRU(input_shape_list[-1]*input_shape_list[-2], activation='tanh', dropout=dropout_rate,
#             recurrent_dropout=dropout_rate, return_sequences=True)(y)
#     model = Model(inputs=x, outputs=y)
#     model.summary()
#     y = Reshape(input_shape, name='predictions')(y)
#     y = keras.activations.softmax(y, axis=1)
#
#     model = Model(inputs=x, outputs=y)
#     model.compile(optimizer='Adam', loss='binary_crossentropy',
#                   metrics=['accuracy'])
#     model.summary()
#     return model

def sample(adj_mat_row, d):
    node_part = adj_mat_row[:d.node_one_hot_vector_size]
    edge_part = adj_mat_row[d.node_one_hot_vector_size:]
    edge_part = np.reshape(edge_part, (d.M, d.edge_one_hot_vector_size))

    out_node_part = np.zeros((d.node_one_hot_vector_size,))
    a = np.random.choice(d.node_one_hot_vector_size, 1, node_part.tolist())
    out_node_part[a] = 1

    out_edge_part = np.zeros((d.M, d.edge_one_hot_vector_size))
    for i in range(d.M):
        out_edge_part[i, int(np.random.choice(
            d.edge_one_hot_vector_size, 1, edge_part[i].tolist())[0])] = 1

    out_edge_part = np.reshape(
        out_edge_part, (d.M * d.edge_one_hot_vector_size,))
    return np.concatenate((out_node_part, out_edge_part))


def generate(model, d, batch_size):
    # init starting graph input
    nodes_input = np.zeros(d.node_one_hot_vector_size)
    # SOS
    nodes_input[0] = 1
    edges_input = np.zeros((d.M, d.edge_one_hot_vector_size))
    # NO_EDGE
    edges_input[:, 0] = 1
    edges_input = np.reshape(edges_input, (d.M * d.edge_one_hot_vector_size,))
    combined_input = np.concatenate((nodes_input, edges_input))
    X = np.zeros((batch_size, d.max_nodes, d.node_one_hot_vector_size +
                  d.edge_one_hot_vector_size*d.M))
    for i in range(batch_size):
        X[i, 0, :] = combined_input

    for i in range(d.max_nodes-1):
        ys = model.predict(X)
        for idx, y in enumerate(ys):
            y = sample(y[i, :], d)
            X[idx, i + 1, :] = y
            # if y[1] == 1:
            #     break

    return X
