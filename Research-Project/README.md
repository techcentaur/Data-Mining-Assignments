### Graph RNN

Generating graphs representing chemical compounds

## Interface

Training dataset set through config.yml in yaml format as follows
```yaml
data:
  filepath: <path of training dataset (if relative then w.r.t main.py)>
```

The training procedure can be done by executing the below command
```sh
python main.py
```

## Approach

### Initial approach

Our Approach is derived from GraphRNN described in the paper <link>

We started by making a model that would produce only the structure of the compound, i.e. adjacency matrix of the corresponding graph without any labels. Once we have a working copy of this model, We were planning to add label prediction to that. But as we started implementing this, we realized that a model that takes the labels of previously generated nodes and edges would be better. That way, the hidden state of the RNN would store a pattern that takes into account every aspect of the graph before, not just only the skeletal structure.

So going forward, our approach is the following:

### Design of the Model
Our model is an autoregressive model which utilizes two RNNs,

#### 1. Node-level RNN
This one generates nodes and their labels. In the case of chemical compounds the labels are the atom / chemical element. We would create a vocabulary of all the atoms that appears in the given training dataset. Also, there would be two extra tokens in the vocabulary, `SOS` and `EOS`, signifying the start and the end of sequence respectively.

The input to this RNN will be one-hot encoded version of the nodes, in a random BFS order like it was described in the paper. Also, as the model is an RNN, the hidden state of a particular time step will be fed back into the model in the next time-step, thereby storing the temporal relation present in the sequence of nodes in the hidden state. 

#### 2. Edge-level RNN
This model is for generating edges and their labels, in the case of chemical compunds the labels being the numer of bonds. We will create the adjacency matrix in such a way so that the edge labels are also encoded in that. This can be done by making the matrix 3D instead of 2D, the third dimension storing the edge label in an one-hot encoded fashion.

Once we have this model, we will trim this matrix so that redundant information arising out of BFS ordering gets removed, just like it's described in the paper. 

The RNN would also take the activation of the node-level RNN at the same time-step as input.

### Novel Graph Generation

The output of the RNNs are softmax probability distribution over the vocabulary. So at the time of generating new nodes and edges, we would sample from that distribution.


### Team Members
- Ankit Solanki 2016CS50401
- Sumit Ghosh 2016CS50400
- Yash Malviya 2016CS50403
