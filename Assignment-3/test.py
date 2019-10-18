"""
Generating graphs
"""
import torch as tch
from config import config

from torch.autograd import Variable


def testing(model1, model2, processor):
    model1.eval()
    model2.eval()

    Ypredictions = Variable(tch.zeros(
            config["test"]["batch_size"],
            processor.maxnodes,
            processor.trunc_length))

    step = Variable(tch.ones(
        config["test"]["batch_size"],
        1, processor.trunc_length
        ))
    for node in range(processor.maxnodes):
        # take hidden state of model1 (graph/node-level rnn) provide
        # it to model2 (edge-level rnn)
        out1 = model1(step, packed_sequence=False)
        out1size = out1.size()
        print(out1size)

        # batch_size comes to first in rnn module
        model2.hidden = tch.cat(
                (out1.permute(1, 0, 2),
                Variable(tch.zeros(
                    model2.params["num_layers"]-1, out1size[0], out1size[2]
                    ))),
                dim=0)

        Xin = Variable(tch.ones(config["test"]["batch_size"], 1, model2.params["input_size"]))
        Xout = Variable(tch.zeros(config["test"]["batch_size"], 1, processor.trunc_length))
        
        # TODO: add sample_sigmoid to model.py
        for j in range(min(processor.trunc_length, node+1)):
            tmp = model2(Xin, packed_sequence=False)
            # function not implemented
            Xin = processor.sampling(tmp, sample=True, sample_time=1)

            Xout[:, :, j] = Xin
            model2.hidden = Variable(model2.hidden.data)

        Ypredictions[:, node, :] = Xout
        model1.hiddden = Variable(model1.hidden.data)
    _Ypredictions_ = Ypredictions.data.long()

    predicted_graphs = []
    for i in range(config["test"]["batch_size"]):
        # function not implemented
        m = processor.convert_from_sequence(_Ypredictions_[i])
        # function not implemented
        predicted_graphs.append(processor.sequence_to_graph(m))

    outfile = "predicted_graph_tests_file.dat"
    with open(outfile, "wb") as f:
        # pickle.dump(out, f)
        f.write(str(predicted_graphs))

    print("[!] Graph saved in: `{}`".format(outfile))