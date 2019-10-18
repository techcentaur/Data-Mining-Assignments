import torch
from torch import nn

from torch.autograd import Variable
from torch.nn.utils.rnn import (pad_packed_sequence, pack_padded_sequence)

class GRUModel(nn.Module):

    def __init__(self, params):
        super().__init__()
        self.params = params

        self.hidden = None
        self.layer1 = nn.GRU(
                    input_size=self.params["input_size"],
                    hidden_size=self.params["hidden_size"],
                    num_layers=self.params["num_layers"],
                    batch_first=True,
                    bias=True)
        self.layer2 = nn.Linear(
                    in_features=self.params["hidden_size"],
                    out_features=self.params["output_size"],
                    bias=True)

    def forward(self, X):
        X, self.hidden = self.layer1(X, self.hidden)
        X = pad_packed_sequence(X, batch_first=True)[0]
        X = self.layer2(X)
        return X
