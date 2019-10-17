"""
Generating graphs
"""
import torch as tch
from torch.autograd import Variable
from config import config

from model import *


def testing(params):
    model1 = params["model1"]
    model2 = params["model2"]

    # set models to eval mode
    model1.eval()
    model2.eval()

    num_of_layers = int(config['nn']['num_of_layers'])

    # loaded to calculate dimensions of data to input
    batch_size = params["batch_size"]
    maxnodes = params["maxnodes"]
    trunc_length = params["trunc_length"]

    pred_y = Variable(
        tch.zeros(batch_size, maxnodes, trunc_length)).cuda()
    step_x_inp = Variable(tch.ones(batch_size, 1, trunc_length)).cuda()

    # generation algo loop
    for i in range(maxnodes):
                # take hidden state of model1 (graph/node-level rnn) provide
                # it to model2 (edge-level rnn)
        mod1_HS = model1(step_inp)
        HSsize = mod1_HS.size()
        hz = Variable(
            tch.cat(tch.zeros(num_of_layers - 1, HSsize[0], HSsize[2]))).cuda()
        model2.hidden = tch.cat((mod1_HS.permute(1, 0, 2), hz), dim=0)
        step_x_inp = Variable(tch.zeros(batch_size, 1, trunc_length)).cuda()
        step_x_outp = Variable(tch.ones(batch_size, 1, 1)).cuda()
        for j in range(min(trunc_length, i+1)):
                pred_y_outp = model2(step_x_outp)
                # TODO: add sample_sigmoid to model.py
                step_x_outp = sample_sigmoid(
                    pred_y_outp, sample=True, sample_time=1)
				x_step[:, :, j:j+1] = step_x_outp
				model2.hidden = Vairal(model2.hidden.data).cuda()
			pred_y[:, i:i + 1, :] = x_step
			model1.hiddden = Variable(model1.hidden.data).cuda()
			pred_y_data = pred_y.data.long()

			# complete 
			# save graph as pickle in local var

			# return the saved graphs
