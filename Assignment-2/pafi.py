"""
Converting from given format of dataset into PAFI format
"""


def change_format(filepath, outfile=None, verbose=False):
	"""change given format to pafi format"""

	if verbose:
		print("[*] Converting file: {} into PAFI(FSG) format\n".format(filepath))

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
			res.append("t\n")
			i += 1
		else:
			if new_graph:
				new_graph = False
				numv = int(content[i])

				for j in range(1, numv+1):
					res.append("v {node} {label}".format(node=str(j-1), label=content[i+j]))
				i = i+numv+1

			elif not new_graph:
				nume = int(content[i])
				nume = int(nume)

				for j in range(1, nume+1):
					res.append("u {}".format(content[i+j]))
				i = i+nume+1	
			else:
				i+=1

	if not outfile:
		outfile = "./Yeast/pafi_{}".format(filepath.split("/")[-1])

	with open(outfile, 'w') as f:
		f.write(''.join(res))
	if verbose:
		print("[*] File saved in: {}".format(outfile))

	return outfile

if __name__ == '__main__':

	file = "./Yeast/smol.txt_graph"
	change_format(file, verbose=True)