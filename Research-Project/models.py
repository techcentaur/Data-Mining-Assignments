from keras.layers import GRU, Activation, Input, Reshape
from keras import Model
import keras
import functools
import operator
import numpy as np


DROPOUT_RATE = 0.5
NODES_LAYERS_DMS = [2, 4]
EDGES_LAYERS_DMS = [2, 4]


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


model = edge_gru((10, 20))
model.fit(np.random.rand(32, 10, 20), np.random.rand(32, 10, 20), batch_size=8)
