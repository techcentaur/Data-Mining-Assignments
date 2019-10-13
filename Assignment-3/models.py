"""
All models have to be implemented here
models for
1. output
2. rnn

"""
import torch
from torch import (nn, zeros)
from torch.nn.utils.rnn import (pad_packed_sequence, pack_padded_sequence)
from torch.nn.autograd import Variable

class GRUModel(nn.Module):
    def __init__(self, params):
        super().__init__()

        self.params = params

        self.hidden = None
        self.layer1 = nn.Linear(
                    in_features=self.params["inputsize"],
                    out_features=self.params["outputtmp"],
                    bias=True
                    )
        self.relu = nn.ReLU()
        self.layer2 = nn.GRU(
                    input_size=self.params["outputtmp"],
                    hidden_size=self.params["hiddensize"],
                    num_layers=self.params["numlayers"],
                    batch_first=True, #(batch, seq, feature)
                    bias=True
                    )
        self.layer3 = nn.Sequential(
                nn.Linear(self.params["hiddensize"], self.params["outputtmp"]),
                nn.ReLU(),
                nn.Linear(self.params["outputtmp"], self.params["outputsize"])
            )

    def _hidden_(self, batch_size):
        arr = torch.zeros(
                self.params["num_layers"],
                batch_size,
                self.params["hidden_size"]
                )
        return Variable(arr)
    
    def forward(self, X, l):
        X = self.layer1(X)
        X = self.relu(X)

        X = pack_padded_sequence(X, l, batch_first=True)
        X, self.hidden = self.layer2(X, self.hidden)
        
        X = pad_packed_sequence(X, batch_first=True)
        X = X[0] # we got a tuple of X, lengths list
        
        X = self.layer3(X)
        return X
