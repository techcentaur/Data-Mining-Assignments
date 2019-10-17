import torch as tch
from datetime import datetime

from data import Data
from train import train
from config import config
from models import GRUModel
from processing import DataProcessor

if __name__ == '__main__':
	now = datetime.now()
	print("[*] Graph Generative Model: GraphRNN\n")
	print("[-] Starting @ {}!".format(now.strftime("%Y-%m-%d %H:%M:%S")))

	data = Data()
	graphs = data.get_graphs()
	print("[*] Graph dataset loaded: {} graphs".format(len(graphs)))

	# implement function for dataset sampler
	processor = DataProcessor(graphs)
	dataloader = tch.utils.data.DataLoader(
					processor,
					batch_size=config["batch"])

	params = {
		"input_size": processor.trunc_length,
		"num_layers": 4,
		"hidden_size": 128,
		"num_directions": 1,
		"output_size": 16
	}
	model1 = GRUModel(params)

	params = {
		"input_size": 1,
		"hidden_size": 16,
		"num_layers": 4,
		"num_directions": 1,
		"output_size": 1
	}
	model2 = GRUModel(params)

	# # implement training wrapper function
	train(model1, model2, dataloader, processor)
