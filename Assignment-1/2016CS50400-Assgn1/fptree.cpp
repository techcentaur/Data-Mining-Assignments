// FP-tree implementation

#include<iostream>
#include<fstream>
#include<set>
#include<vector>
#include<unordered_map>
#include<sstream>

using namespace std;

struct Node{
	int count;
	int label;
	vector<Node*> children;
	Node* parent;
	
	Node(int l, int c, Node* p){
		this->label = l;
		this->count = c;
		this->parent = p;
	}
};

unordered_map<int, int> itemsMap;

// Scan transaction DB and return unordered map of itemID to frequency
void getFlist(ifstream& file){
    string line;
    while (getline(file, line)){
        stringstream lineStream(line);
        int value;

        while (lineStream >> value){
            if(itemsMap.find(value) != itemsMap.end()){
            	itemsMap[value]++;
            }else{
            	itemsMap[value] = 1;
            }
        }
   }
}


bool cmpFunc(const int a, const int b) {
    if(itemsMap[a] >= itemsMap[b]) return true;
    else false;
    return false;
}

class cmp{
public:
    bool operator() (const int a, const int b) const {
        return cmpFunc(a, b);
    }
};

class Tree{
public:
	Node* root;
	vector<vector<Node*>> pointerTable;
	unordered_map<int, int> indexes;
	int sizeOfPointers;

	Tree(){
		this->root = new Node(-1, -1, NULL);  // NULL node
		int i=0;
		for(auto it: itemsMap){
			vector<Node*> v;
			// according to frequency
			this->indexes[it.first] = i;
			this->pointerTable.push_back(v); 
			i++;
		}
		this->sizeOfPointers = i;
	}

	void insertInTree(Node* root, set<int, cmp>& trans, set<int>::iterator i){
		if(i == trans.end()){return;}

		for(auto& child: root->children){
			if(child->label == *i){
				child->count += 1;
				insertInTree(child, trans, ++i);
				return;
			}
		}

		Node* newNode = new Node(*i, 1, root);  // new Node: trans.at(i)->label, 1->freq, root->parent
		root->children.push_back(newNode);
		this->pointerTable[this->indexes[*i]].push_back(newNode);  // put it in pointerTable
		
		insertInTree(newNode, trans, ++i);
		return;
	}

	void printItOut(){
		cout<<"Root: "<<root->label<<endl;
		cout<<"pointerTable: \n";
		cout<<this->pointerTable.size()<<endl;
		for(int i=0; i<pointerTable.size(); i++){
			cout<<"Size: "<<pointerTable[i].size()<<endl;
			cout<<"Label: "<<pointerTable[i][0]->label<<endl;
			for(int j=0; j<pointerTable[i].size(); j++){
				cout<<"L: "<<pointerTable[i][j]->label<<" C: "<<pointerTable[i][j]->count<<endl;
			}
		}
		for(auto& i: pointerTable){
			for(int j=0; j<i.size(); j++){
				cout<<"L: "<<i[j]->label<<" C: "<<i[j]->count<<", ";
			}
			cout<<endl;
		}
		cout<<"Size: "<<sizeOfPointers<<endl;
		cout<<"Indexes: \n";
		for(auto i: indexes){
			cout<<i.first<<" "<<i.second<<endl;
		}
	}

};


Tree* plantTree(ifstream& file, int& dbSize){
    string line;
	Tree* greenWood = new Tree();
	dbSize = 0;
    
    while (getline(file, line)){
        stringstream lineStream(line);
        set<int, cmp> trans;
        int value;
        
        while (lineStream >> value){
            trans.insert(value);
        }

        set<int>::iterator it = trans.begin();
        greenWood->insertInTree(greenWood->root, trans, it);
		dbSize++;
   }
   return greenWood;
}

vector<set<int>> anotherTraverse(int idx, Tree* t, const int& support, const int& whichLabel){
	unordered_map<int, int> condCounter;
	int currentIDCount = 0;
	int currentIDLabel = whichLabel;

	for(int i=0; i<t->pointerTable[idx].size(); i++){
		Node* leaf = t->pointerTable[idx][i];
		int currentIDInitialCount = leaf->count;

		while(leaf->label!=-1){
			if(leaf->label == whichLabel){
				currentIDCount += currentIDInitialCount;
				while(leaf->label != -1){
					if(condCounter.find(leaf->label) != condCounter.end()){
						condCounter[leaf->label] += currentIDInitialCount;
					}else{
						condCounter[leaf->label] = currentIDInitialCount;
					}
					leaf = leaf->parent;
				}
			}
			else{
				leaf = leaf->parent;
			}
		}
	}

	if(currentIDCount >= support){
		vector<set<int>> v;
		set<int> n;
		n.insert(currentIDLabel);
		v.push_back(n);

		vector<int> freqLabels;
		for(auto& l: condCounter){
			if((l.second >= support) && (l.first != currentIDLabel)){
				freqLabels.push_back(l.first);
			}
		}

		for(int label: freqLabels){
			vector<set<int>> tmp;
			tmp = anotherTraverse(idx, t, support, label);
			for(set<int>& supertmp: tmp){
				supertmp.insert(currentIDLabel);
				v.push_back(supertmp);
			}
		}
		return v;

	}else{
		vector<set<int>> vv;
		return vv;
	}

}


void traverse(int idx, Tree* t, const int& support, vector<set<int>>& freqsets){
	unordered_map<int, int> condCounter;
	int currentIDCount = 0;
	int currentIDLabel = t->pointerTable[idx][0]->label;
	for(int i=0; i<t->pointerTable[idx].size(); i++){
		Node* leaf = t->pointerTable[idx][i];
		int currentIDInitialCount = leaf->count;
		currentIDCount += leaf->count;
		while(leaf->label != -1){
			if(condCounter.find(leaf->label) != condCounter.end()){
				condCounter[leaf->label] += currentIDInitialCount;
			}else{
				condCounter[leaf->label] = currentIDInitialCount;
			}
			leaf = leaf->parent;
		}
	}

	if(currentIDCount >= support){
		set<int> n;
		n.insert(currentIDLabel);
		freqsets.push_back(n);

		vector<int> freqLabels;
		for(auto& l: condCounter){
			if((l.second >= support) && (l.first != currentIDLabel)){
				freqLabels.push_back(l.first);
			}
		}

		for(int label: freqLabels){
			vector<set<int>> tmp;
			tmp = anotherTraverse(idx, t, support, label);
			for(set<int>& supertmp: tmp){
				supertmp.insert(currentIDLabel);
				freqsets.push_back(supertmp);
			}
		}
	}
	return;
}

void getFrequentSets(vector<set<int>>& itemsets, int support, Tree* t){
	int size = t->pointerTable.size();
	for (int i=0; i<t->pointerTable.size(); i++){
		if(t->pointerTable[i].size()>0){
			traverse(i, t, support, itemsets);
		}
	}
}

int main(int argc, char* argv[]){
	// argv[] = dataFile outFile percentageThresh
	ifstream dataFile;
	dataFile.open(argv[1]);
	getFlist(dataFile);

	dataFile.clear();
    dataFile.seekg(0, ios::beg);

	int dbSize = 0;
	Tree* t = plantTree(dataFile, dbSize);
	int suppThresh = (atof(argv[3])*dbSize)/100;
	vector<set<int>> minedItemSets; 
	
	getFrequentSets(minedItemSets, suppThresh, t);
	dataFile.close();

	ofstream outFile;
	outFile.open(argv[2]);
	for (set<int>& freqSet: minedItemSets) {
		for (auto it=freqSet.begin(); it!=freqSet.end(); it++) {
			outFile << *it;
			if (it!=--freqSet.end()) {
				outFile << " ";
			}
		}
		outFile << endl;
	}

	return 0;
}
