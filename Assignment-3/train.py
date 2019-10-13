from config import config
import numpy as np
import torch as t

import time


def train_rnn_epoch(epoch, rnn, output, data_loader,
                    optimizer_rnn, output_optimizer,
                    rnn_scheduler, output_scheduler):
    rnn.train()
    output.train()
    sum_of_loss = 0
    for batch_id, dict_data in enumerate(data_loader):
        # set models param's gradients to zero
        rnn.zero_grad()
        output.zero_grad()

        # get x and y to desired formats
        # unsorted x, y as floats
        x = dict_data['x'].float()
        y = dict_data['y'].float()

        y_length = dict_data['len']
        max_y_length = max(y_length)

        # truncated till max len
        x = x[:, 0:max_y_length, :]
        y = y[:, 0:max_y_length, :]

        # initialize hidden state
        rnn.hidden = rnn.init_hidden(batch=x.size(0))

        # sorting
        # desc sort according to num of nodes in graph
        y_length, index_rearrangement = t.sort(y_length, 0, descending=True)
        
        x = t.index_select(x, 0, index_rearrangement)
        y = t.index_select(y, 0, index_rearrangement)
        y_length = y_length.numpy().tolist()

        


def test_rnn_epoch(epoch, rnn, output, test_batch_size=16):
    pass


def train_rnn_forward_epoch(epoch, rnn, output, data_loader):
    pass


def train(args, dataset_train, rnn, output):
    epoch = 1

    # optimizer and schedulers
    rnn_optimizer = optim.Adam(
        list(rnn.parameters()), lr=config['train']['lr'])
    output_optimizer = optim.Adam(
        list(output.parameters()), lr=config['train']['lr'])

    rnn_scheduler = MultiStepLR(
        rnn_optimizer, milestones=config['train']['milestones'], gamma=config['train']['lr_rate'])
    output_scheduler = MultiStepLR(
        output_optimizer, milestones=config['train']['milestones'], gamma=config['train']['lr_rate'])

    # epoch loops
    # save epoch timings
    epoch_timings = np.zeros(config['train']['epochs'])

    while epoch <= config['train']['epochs']:
        time_start = time.time()
        # training
        train_rnn_epoch(epoch, rnn, output, dataset_train, rnn_optimizer,
                        output_optimizer, rnn_scheduler, output_scheduler)
        # testing

        # saving model checkpoints

        epoch_timings[epoch-1] = time.time() - time_start
