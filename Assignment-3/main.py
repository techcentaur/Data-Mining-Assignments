import torch as tch
from datetime import datetime

from data import Data
from train import train
from config import config
from models import GRUModel
from graphrnn import GraphRNNLoader

if __name__ == '__main__':
	now = datetime.now()
	print("[*] Processing the data... @ {}!".format(now.strftime("%Y-%m-%d %H:%M:%S")))

	d = Data()
	graphobjects = d.get_graphs()

	# print("[*] ")

	# implement function for dataset sampler
	loader = GraphRNNLoader(graphobjects)
	dataloader = tch.utils.data.DataLoader(
					loader,
					batch_size=config["batch_size"]
					)

	params = {
		"inputsize": loader.trunc_length,
		"outputtmp": 64,
		"hiddensize": 128,
		"numlayers": 4,
		"outputsize": 16
	}
	model1 = GRUModel(params)

	params = {
		"inputsize": 1,
		"outputtmp": 8,
		"hiddensize": 16,
		"numlayers": 4,
		"outputsize": 1
	}
	model2 = GRUModel(params)

	# implement training wrapper function
	train(model1, model2, dataloader, loader)
