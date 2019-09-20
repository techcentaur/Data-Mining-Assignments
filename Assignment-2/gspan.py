import json

def change_format(filepath, outfile=None, verbose=False):
	if verbose:
		print("[*] Converting file: {} into Gaston format\n".format(filepath))

	enum = 0

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

			res.append("t # {}\n".format(enum))
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
		outfile = "./gspan_{}".format(filepath.split("/")[-1])

	with open(outfile, 'w') as f:
		f.write(''.join(res))
	if verbose:
		print("[*] File saved in: {}".format(outfile))

	return outfile

if __name__ == '__main__':

	
	file = "./Yeast/smol.txt_graph"
	change_format(file, verbose=True)