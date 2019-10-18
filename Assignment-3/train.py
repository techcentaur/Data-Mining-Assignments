import time
import torch as tch
import numpy as np

import test
from config import config

import torch.nn.functional as F
from torch import optim
from torch.autograd import Variable
from torch.optim.lr_scheduler import MultiStepLR
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence

def get_pack_length(Y, L):
    packlength = []
    packed = np.bincount(np.array(L).astype('int64'))
    for i in range(len(packed)-1, 0, -1):
        tmp = np.sum(packed[i:])
        packlength.extend([min(i, tch.FloatTensor(Y).size(2))] * tmp)
    return packlength

def ____training____(params, loader):
    model1 = params["model1"]
    model2 = params["model2"]
    dataloader = params["data_loader"]

    model1.train()
    model2.train()

    for i, d in enumerate(dataloader):
        model1.zero_grad()
        model2.zero_grad()

        sequence_list = d['seq'].float()
        values = {'X': [], 'Y': [], 'L': []}

        for seq in sequence_list:
            Xdatum = np.zeros((params["processor"].maxnodes, params["processor"].trunc_length))
            Ydatum = np.zeros((params["processor"].maxnodes, params["processor"].trunc_length))

            Xdatum[0, :] = 1

            Xdatum[1: seq.size()[0], :] = seq[0: seq.size()[0]-1, :]
            Ydatum[0: seq.size()[0], :] = seq

            values['X'].append(Xdatum)
            values['Y'].append(Ydatum)
            values['L'].append(seq.shape[0])

        # syntax of using pack_padded_sequence
        values['X'] = [x[0: max(values['L']), :] for x in values['X']]
        values['Y'] = [x[0: max(values['L']), :] for x in values['Y']]

        model1.hidden = Variable(
                    tch.zeros(model1.params["num_layers"] * model1.params["num_directions"],
                    len(values['L']),
                    model1.params["hidden_size"]))

        Ypackpad = pack_padded_sequence(
            tch.FloatTensor(values['Y']),
            tch.FloatTensor(values['L']),
            batch_first=True).data
        Ypacksize = Ypackpad.size()
        Ypackpad = Ypackpad.view(Ypacksize[0], Ypacksize[1], 1)

        X1 = Variable(tch.FloatTensor(values['X']))
        Y1 = Variable(tch.FloatTensor(values['Y']))
        X2 = Variable(tch.cat((
            tch.ones(Ypackpad.size(0), 1, 1),
            Ypackpad[:, 0:-1, :]),
            dim=1))
        Y2 = Variable(Ypackpad)

        assert X2.shape==Y2.shape

        X1 = pack_padded_sequence(X1, values['L'], batch_first=True, enforce_sorted=False)
        X1out = model1(X1)
        # print(X1out.shape)
        # batch seq hiddensize

        X1outpacked = pack_padded_sequence(X1out, values['L'], batch_first=True).data
        HSsize = X1outpacked.size()

        newhidden = Variable(
            tch.zeros(
                model2.params["num_layers"]-1,
                HSsize[0],
                HSsize[1]))

        model2.hidden = tch.cat(
                (X1outpacked.view(1, HSsize[0], HSsize[1]),
                    newhidden
                ), dim = 0)
        pl = get_pack_length(values['Y'], values['L'])

        outY = pack_padded_sequence(X2, pl, batch_first=True, enforce_sorted=False)
        outY = model2(outY)
        outY = tch.sigmoid(outY)

        loss = F.binary_cross_entropy(outY, Y2)
        loss.backward()

        params["m2_opt"].step()
        params["m1_opt"].step()

        params["m2_sched"].step()
        params["m1_sched"].step()

        print("loss: {}".format(loss.tolist(), loss))

def train(model1, model2, data_loader, processor):

    # optimizer and schedulers
    model1_optimizer = optim.Adam(
        list(model1.parameters()),
        lr=config['train']['lr'])
    model2_optimizer = optim.Adam(
        list(model2.parameters()),
        lr=config['train']['lr'])

    model1_scheduler = MultiStepLR(
        model1_optimizer,
        milestones=config['train']['milestones'],
        gamma=config['train']['lr'])
    model2_scheduler = MultiStepLR(
        model2_optimizer,
        milestones=config['train']['milestones'],
        gamma=config['train']['lr'])

    epoch = 0
    while epoch <= config['train']['epochs']:
        time_start = time.time()

        params = {
            "data_loader": data_loader,
            "processor": processor,
            "model1": model1,
            "model2": model2,
            "m1_opt": model1_optimizer,
            "m2_opt": model2_optimizer,
            "m1_sched": model1_scheduler,
            "m2_sched": model2_scheduler
        }
        ____training____(params, processor)

        # print("[*] Epoch {} | Time {}".format(epoch+1, time.time() - time_start))
        epoch += 1

    ## give the model a test run
    test.testing(model1, model2, processor)