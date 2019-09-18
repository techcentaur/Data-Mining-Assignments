import json


def shorten_dataset(count=100, outfile=None):
	"""shorten the dataset upto count transactions and returns the file path"""

	res  = []
	c = 0

	with open("./Yeast/167.txt_graph", 'r') as f:
		for line in f:
			if line.startswith("#"):
				c += 1
			if c > count:
				break
			res.append(line)

	if not outfile:
		outfile = "./Yeast/smol_{}.txt_graph".format(count)
	with open(outfile, 'w') as f:
		f.write(''.join(res))

	return outfile


def change_file_format_for_GASTON(filepath, outfile=None, verbose=False):
	if verbose:
		print("[*] Converting file: {} into Gaston format\n".format(filepath))

	enum = 0
	mapping_ids = {}

	content = []
	with open(filepath, 'r') as f:
		for line in f:
			content.append(line)

	res = []
	i = 0
	while i < len(content):
		x = (content[i][:-1])
		if not x:
			i += 1
			continue

		if content[i].startswith("#"):
			new_graph=True

			mapping_ids[content[i][1:-1]] = enum
			res.append("# t {}\n".format(enum))
			enum += 1
			i += 1
		else:
			if new_graph:
				new_graph = False
				numv = int(content[i])

				nodemapcount = 0
				nodemap = {}

				for j in range(1, numv+1):
					if content[i+j] in nodemap:
						res.append("v {node} {label}\n".format(node=str(j-1), label=nodemap[content[i+j]]))
					else:
						nodemap[content[i+j]] = nodemapcount
						res.append("v {node} {label}\n".format(node=str(j-1), label=nodemap[content[i+j]]))
						nodemapcount+=1
						
				i = i+numv+1

			elif not new_graph:
				nume = int(content[i])
				nume = int(nume)

				for j in range(1, nume+1):
					res.append("e {}".format(content[i+j]))
				i = i+nume+1	
			else:
				i+=1

	if not outfile:
		outfile = "./Yeast/gaston_{}".format(filepath.split("/")[-1])

	with open(outfile, 'w') as f:
		f.write(''.join(res))
	if verbose:
		print("[*] File saved in: {}".format(outfile))

	# write mapping too
	out = outfile.split("/")
	out[-1] = "mapping_"+out[-1]
	dictfile = "/".join(out)

	with open(dictfile, 'w') as f:
		f.write(json.dumps(mapping_ids))

	if verbose:
		print("[-] Mapping saved as: {}".format(dictfile))

	return outfile

if __name__ == '__main__':

	file = "./Yeast/smol.txt_graph"
	change_file_format_for_GASTON(file, verbose=True)