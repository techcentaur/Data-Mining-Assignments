from config import config
from data import Data
from datetime import datetime


if __name__ == '__main__':
	

	now = datetime.now()
	print("[*] Processing the data... @ {}!".format(now.strftime("%Y-%m-%d %H:%M:%S")))

	d = Data()
	graphobjects = d.get_graphs()


	# update config variables if needed 
	# print the necessary information


	# implement function for dataset sampler
	# dataset = graphRNN_dataloader(graphobjects)


	# implement conversion to pytorch dataloader object
	# data_loader = torch.utils.data.Dataloader(dataset)


	# define pytorch - models here
	# models for:
	#	1. output
	#	2. rnn


	# implement training wrapper function
	# train(data_loader, output_model, rnn_model)