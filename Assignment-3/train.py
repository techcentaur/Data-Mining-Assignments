import test
from config import config

import time
import torch as tch
import numpy as np
from torch import optim
import torch.nn.functional as F

from torch.autograd import Variable
from torch.nn.utils.rnn import (pad_packed_sequence, pack_padded_sequence)

def train(model1, model2, data_loader, processor):

    model1_optimizer = optim.Adam(
        list(model1.parameters()),
        lr=config['train']['lr'])
    model2_optimizer = optim.Adam(
        list(model2.parameters()),
        lr=config['train']['lr'])

    epoch = 0
    while epoch <= config['train']['epochs']:
        ____training____(
            data_loader=data_loader,
            processor=processor,
            model1=model1,
            model2=model2,
            m1_opt=model1_optimizer,
            m2_opt=model2_optimizer)

        epoch += 1

    test.testing(model1, model2, processor)

def ____training____(data_loader, processor,
                    model1, model2,
                    m1_opt, m2_opt):
    model1.train()
    model2.train()

    for i, d in enumerate(data_loader):
        model1.zero_grad()
        model2.zero_grad()

        seq_list = d['seq'].float()
        v = {'X': [], 'Y': [], 'L': []}

        for seq in seq_list:
            X_ = np.zeros((processor.max_nodes, processor.M))
            Y_ = np.zeros((processor.max_nodes, processor.M))

            X_[0, :] = 1

            X_[1: seq.size()[0], :] = seq[0: seq.size()[0]-1, :]
            Y_[0: seq.size()[0], :] = seq

            v['X'].append(X_)
            v['Y'].append(Y_)
            v['L'].append(seq.shape[0])

        v['X'] = tch.FloatTensor(v['X'])
        v['Y'] = tch.FloatTensor(v['Y'])
        
        X1 = Variable(v['X'])
        Y1 = Variable(v['Y'])

        model1.hidden = Variable(tch.zeros(model1.params["num_layers"]*model1.params["num_directions"],
                    len(v['L']), model1.params["hidden_size"]))

        X1out = model1(pack_padded_sequence(X1, v['L'], batch_first=True, enforce_sorted=False))
        X1outpacked = pack_padded_sequence(X1out, v['L'], batch_first=True).data

        Ypackpad = pack_padded_sequence(v['Y'], v['L'], batch_first=True).data
        Ypackpad = Ypackpad.view(Ypackpad.shape[0], Ypackpad.shape[1], 1)

        X2 = Variable(tch.cat((tch.ones(Ypackpad.size(0), 1, 1),
            Ypackpad[:, 0:-1, :]), dim=1))
        Y2 = Variable(Ypackpad)

        assert X2.shape==Y2.shape
        HSsize = X1outpacked.size()

        newhidden = Variable(tch.zeros(
                model2.params["num_layers"]-1, HSsize[0], HSsize[1]))
        model2.hidden = tch.cat(
                (X1outpacked.view(1, HSsize[0], HSsize[1]), newhidden), dim = 0)

        outY = pack_padded_sequence([X2.shape[1]]*X2.shape[0], pl, batch_first=True, enforce_sorted=False)
        outY = tch.sigmoid(model2(outY))

        loss = F.binary_cross_entropy(outY, Y2)
        loss.backward()

        m2_opt.step()
        m1_opt.step()

        print("loss: {}".format(loss.tolist(), loss))
