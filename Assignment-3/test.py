"""
Generating graphs
"""

def testing(params):
	model1 = params["model1"]
	model2 = params["model2"]

	model1.eval()
	model2.eval()

	maxnodes = int(params["maxnodes"])

	for i in range(maxnodes):
		H = model1(X)

		
