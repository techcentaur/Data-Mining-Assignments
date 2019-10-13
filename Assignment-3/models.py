"""
All models have to be implemented here
models for
1. output
2. rnn

"""
import torch
from torch import nn
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence


class GRUModel(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, output_size, num_layers):
        super().__init__()

        self.input = nn.Linear(input_size, embedding_size)
        self.rnn = nn.GRU(input_size=embedding_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.output = nn.Sequential(
                nn.Linear(hidden_size, embedding_size),
                nn.ReLU(),
                nn.Linear(embedding_size, output_size)
            )
        self.relu = nn.ReLU()
        self.hidden = None

        for name, param in self.rnn.named_parameters():
            if 'bias' in name:
                nn.init.constant(param, 0.25)
            elif 'weight' in name:
                nn.init.xavier_uniform(param, gain=nn.init.calculate_gain('sigmoid'))
        for m in self.modules():
            if isinstance(m, nn.Linear):
                m.weight.data = nn.init.xavier_uniform(m.weight.data, gain=nn.init.calculate_gain('relu'))
        
    def init_hidden(self, batch_size):
        return torch.autograd.Variable(torch.zeros(self.num_layers, batch_size, self.hidden_size))
    
    def forward(self, input_raw, input_len, pack=False):
        x = self.input(input_raw)
        x = self.relu(x)
        if pack:
            x = pack_padded_sequence(x, input_len, batch_first=True)
        output_raw, self.hidden = self.rnn(x, self.hidden)
        if pack:
            output_raw = pad_packed_sequence(output_raw, batch_first=True)[0]
        return self.output(output_raw)
