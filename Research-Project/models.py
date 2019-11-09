from keras.layers import GRU, Activation, Input, Reshape, Concatenate, Lambda
from keras import Model
import keras
import functools
import operator
import numpy as np


DROPOUT_RATE = 0.5
NODES_LAYERS_DMS = (2, 4)
EDGES_LAYERS_DMS = (2, 4)
COMBINED_LAYERS_DMS = (2, 4)


# Input is expected to be flattened concatenated Node Label ohv and edge labels' adjacency list ohv
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
    edge_softmax = Activation(lambda x: keras.activations.softmax(x, 1))(edge_softmax)

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


model = combined_gru(10, 3, 5, 4)
model.fit(np.random.rand(32, 5, 10 + 4*3), np.random.rand(32, 5, 10 + 4*3), batch_size=8)
