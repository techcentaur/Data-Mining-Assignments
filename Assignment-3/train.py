import time
import torch as tch
import numpy as np
from config import config

import torch.nn.functional as F
from torch import optim
from torch.autograd import Variable
from torch.optim.lr_scheduler import MultiStepLR
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence


def ____training____(params, loader):
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
            Xdatum = np.zeros((loader.maxnodes, loader.trunc_length))
            Ydatum = np.zeros((loader.maxnodes, loader.trunc_length))

            Xdatum[0, :] = 1

            Xdatum[1: seq.size()[0], :] = seq[0: seq.size()[0]-1, :]
            Ydatum[0: seq.size()[0], :] = seq

            values['X'].append(Xdatum)
            values['Y'].append(Ydatum)
            values['L'].append(seq.shape[0])

        values['X'] = [x[0: max(values['L']), :] for x in values['X']]
        values['Y'] = [x[0: max(values['L']), :] for x in values['Y']]


        model1.hidden = model1.__hidden__(len(values['L']))
        Y = values['L']
        # Y, sortedindex = tch.sort(
        #     tch.FloatTensor(values['L']),
        #     0,
        #     descending=True
        # )
        # values['X'] = tch.FloatTensor(values['X']).index_select(0, sortedindex)
        # values['Y'] = tch.FloatTensor(values['Y']).index_select(0, sortedindex)

        # Y_reshape = pack_padded_sequence(
        #     values['Y'],
        #     Y.numpy().tolist(),
        #     batch_first=True
        # ).data

        Y_reshape = pack_padded_sequence(
            tch.FloatTensor(values['Y']),
            tch.FloatTensor(values['L']), batch_first=True).data

        # reverse
        # idx = [x for x in range(Y_reshape.size(0)-1, -1, -1)]
        # Y_reshape = Y_reshape.index_select(0, tch.LongTensor(idx))

        # add dimension
        Y_reshape = Y_reshape.view(Y_reshape.size(0), Y_reshape.size(1), 1)
        mod2X = tch.cat((
            tch.ones(Y_reshape.size(0), 1, 1),
            Y_reshape[:, 0:-1, 0:1]),
            dim=1
        )

        mod2Y = Y_reshape

        # don't understand
        yltmp = []
        # print(Y)
        yltmp_ = np.bincount(np.array(Y).astype('int64'))
        for _i in range(len(yltmp_)-1, 0, -1):
            tmp = np.sum(yltmp_[_i:])
            yltmp.extend([min(_i, tch.FloatTensor(values['Y']).size(2))] * tmp)


        X1 = Variable(tch.FloatTensor(values['X']))
        Y1 = Variable(tch.FloatTensor(values['Y']))
        X2 = Variable(mod2X)
        Y2 = Variable(mod2Y)

        # hi in equation algo

        # model1_HS: is the hidden state

        # packed format
        model1_HS = pack_padded_sequence(
            model1(X1, l=Y), Y, batch_first=True).data

        #  reverse h
        # arrange indexes for rearrangement
        indexes = Variable(tch.LongTensor(
            [j for j in range(model1_HS.shape[0] - 1, -1, -1)]))
        model1_HS = model1_HS.index_select(0, indexes)

        # provide hidden state of graph level rnn model1 to edge level rnn model2
        HSsize = model1_HS.size()
        newhidden = Variable(
            tch.zeros(
                model2.params["numlayers"]-1,
                HSsize[0],
                HSsize[1]
                )
            )

        model2.hidden = tch.cat(
                (
                    model1_HS.view(1, HSsize[0], HSsize[1]),
                    newhidden
                ),
                dim = 0
            )
        # print(yltmp)
        outY = tch.sigmoid(model2(X2, l=yltmp))
        outY = pad_packed_sequence(
                pack_padded_sequence(outY, yltmp, batch_first=True),
                batch_first=True
            )[0]

        Y2 = pad_packed_sequence(
                pack_padded_sequence(Y2, yltmp, batch_first=True),
                batch_first=True
            )[0]

        loss = F.binary_cross_entropy(outY, Y2)
        loss.backward()

        params["m2_opt"].step()
        params["m1_opt"].step()

        params["m2_sched"].step()
        params["m1_sched"].step()

        print("loss: {} | f: {}".format(loss.tolist(), loss))


def train(model1, model2, data_loader, loader):

    # optimizer and schedulers
    model1_optimizer = optim.Adam(
        list(model1.parameters()), lr=config['train']['lr'])
    model2_optimizer = optim.Adam(
        list(model2.parameters()), lr=config['train']['lr'])

    model1_scheduler = MultiStepLR(
        model1_optimizer, milestones=config['train']['milestones'], gamma=config['train']['lr_rate'])
    model2_scheduler = MultiStepLR(
        model2_optimizer, milestones=config['train']['milestones'], gamma=config['train']['lr_rate'])

    # save epoch timings
    epoch_timings = np.zeros(config['train']['epochs'])

    # epoch loops
    epoch = 0
    while epoch <= config['train']['epochs']:
        time_start = time.time()

        params = {
            "data_loader": data_loader,
            "model1": model1,
            "model2": model2,
            "m1_opt": model1_optimizer,
            "m2_opt": model2_optimizer,
            "m1_sched": model1_scheduler,
            "m2_sched": model2_scheduler
        }
        ____training____(params, loader)

        # saving model checkpoints
        epoch_timings[epoch-1] = time.time() - time_start
        epoch+=1