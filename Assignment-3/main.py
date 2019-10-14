# modules
from datetime import datetime

# written files
from data import Data
from config import config
from models import GRUModel
from graphrnn import GraphRNNLoader
from train import train

if __name__ == '__main__':
	now = datetime.now()
	print("[*] Processing the data... @ {}!".format(now.strftime("%Y-%m-%d %H:%M:%S")))

	d = Data()
	graphobjects = d.get_graphs()

	# implement function for dataset sampler
	loader = GraphRNNLoader(graphobjects)
    dataloader = torch.utils.data.DataLoader(
    				loader,
	    			batch_size=config["batch_size"],
	    			num_workers=10
	    			)

    params = {
        "inputsize": loader.trunc_length,
        "outputtmp": 64,
        "hiddensize": 128,
        "numlayers": 4,
        "outputsize":
    }
    model1 = GRUModel(params).cuda()

    params = {
        "inputsize": 1,
        "outputtmp": 8,
        "hiddensize": 16,
        "numlayers": 4,
        "outputsize": 1
    }
    model2 = GRUModel(params).cuda()

	# implement training wrapper function
	train(model1, model2, dataloader)
