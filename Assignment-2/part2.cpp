// part-2 code
#include <bits/stdc++.h>
#include <cstdlib>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/vf2_sub_graph_iso.hpp>

using namespace std;

int main(){
	string s = "./pafi-1.0.1/Linux/fsg -s 10.0 -t ./Yeast/pafi_smol.txt_graph";
	const char* command = s.c_str();
	system(command);

	ifstream file;
	f.open("./Yeast/pafi_smol.tid");

	unordered_map<pair<int, int>, int> map;

	int ngraphs = number_of_graphs("./Yeast/pafi_smol.fp")

	vector<vector<bool>> featureVectors(ngraphs);

	string line;
	int numline = 0;
	while(getline(file, line)){
		istringstream iss(line);

		// how to break up string-string 
		string first, hyphen, second;
		iss>>string>>hyphen>>second;
		//

		map[make_pair(atoi(first), atoi(second))] = numline;

		int tmp;
		while(iss>>tmp){
			// rather than appending two binary vector can be XORed
			featureVectors[tmp].push_back(numline);
		}
		numline++;
	}

	// data-structure filled up now

}
