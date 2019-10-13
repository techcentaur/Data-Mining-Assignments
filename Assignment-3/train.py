import time
import torch as tch
import numpy as np

from config import config


def ____training____(params):
    model1 = params["model1"]
    model2 = params["model2"]
    dataloader = params["data_loader"]

    model1.train()
    model2.train()

    for i, d in enumerate(dataloader):
        # set models param's gradients to zero
        model1.zero_grad()
        model2.zero_grad()

        sequence_list = d['seq'].float()

        values = {'X': [], 'Y': [], 'L': []}
        for seq in sequence_list:
            Xdatum = np.zeros((dataloader.maxnodes, dataloader.trunc_length))
            Ydatum = np.zeros((dataloader.maxnodes, dataloader.trunc_length))

            X[0, :] = 1
            Xdatum[1: seq[0]+1, :] = seq
            Ydatum[0: seq[0], :] = seq

            values['X'].append(Xdatum)
            values['Y'].append(Ydatum)
            values['L'].append(seq.shape[0])

        values['X'] = values['X'][:, 0: max(values['L']), :]       
        values['Y'] = values['Y'][:, 0: max(values['L']), :]

        model1.hidden = model1.__hidden__(len(values['L']))
        Y, sortedindex = tch.sort(
                    values['L'],
                    0,
                    descending = True
                )
        values['X'] = values['X'].index_select(0, sortedindex)
        values['Y'] = values['Y'].index_select(0, sortedindex)

        Y_reshape = pack_padded_sequence(
                    values['Y'],
                    Y.numpy().tolist()
                    batch_first=True
                    ).data

        # reverse
        idx = [x for x in range(Y_reshape.size(0)-1, -1, -1)]
        Y_reshape = Y_reshape.index_select(0, tch.LongTensor(idx))
        # add dimension
        Y_reshape = Y_reshape.view(Y_reshape.size(0), Y_reshape.size(1), 1)

        mod2X = torch.cat((
                    torch.ones(Y_reshape.size(0), 1, 1),
                    Y_reshape[:, 0:-1, 0:1]),
                dim = 1
                )
        mod2Y = Y_reshape


        # don't understand
        yltmp = []
        yltmp_ = np.bincount(np.array(Y))
        for _i in range(len(yltmp_)-1, 0, -1):
            tmp = np.sum(yltmp_[_i:])
            yltmp.extend([min(_i, values['Y'].size(2))] * tmp)


        X1 = Variable(values['X'])
        Y1 = Variable(values['Y'])
        X2 = Variable(mod2X)
        Y2 = Variable(mod2Y)
        




 

def train(model1, model2, data_loader):

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


        params = {
            "data_loader": data_loader
            "model1": model1,
            "model2": model2
        }
        ____training____(params)


        # saving model checkpoints
        epoch_timings[epoch-1] = time.time() - time_start
