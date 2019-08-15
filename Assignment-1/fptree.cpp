// FP-tree implementation

// #include <bits/stdc++.h>
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
	bool isActive; // 1 to use only these prefixes
	int activeFreq;

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
    // unordered_map<int, int> itemsMap;
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
		this->root = new Node(-1, -1, NULL); // NULL node
		int i=0;
		for(auto it: itemsMap){
			vector<Node*> v;
			// according to frequency
			// cout<<it.first<<" "<<it.second<<endl;
			this->indexes[it.first] = i;
			this->pointerTable.push_back(v); 
			i++;
		}

		this->sizeOfPointers = i;
		// cout<<"size of pointers: "<<this->sizeOfPointers<<endl;
		// cout<<"size of pointer table: "<<this->pointerTable.size()<<endl;
		// this->pointerTable.reserve(this->sizeOfPointers);
	}

	void insertInTree(Node* root, set<int, cmp>& trans, set<int>::iterator i){
		if(i == trans.end()){return;}

		for(auto child: root->children){
			if(child->label == *i){
				child->count += 1;
				insertInTree(child, trans, ++i);
				return;
			}
		}

        // cout<<*i<<endl;
		Node* newNode = new Node(*i, 1, root); // new Node: trans.at(i)->label, 1->freq, root->parent
		root->children.push_back(newNode);
		this->pointerTable[this->indexes[*i]].push_back(newNode); // put it in pointerTable
        // while(true){}
		
		insertInTree(newNode, trans, ++i);
		return;
	}

	void printItOut(){
		cout<<"Root: "<<root->label<<endl;
		cout<<"pointerTable: \n";
		cout<<this->pointerTable.size()<<endl;
		// for(int i=0; i<pointerTable.size(); i++){
		// 	cout<<pointerTable[i].size()<<endl;
		// }
		for(auto i: pointerTable){
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
	        // cout<<value<<endl;
        }
        // cout<<trans.size()<<endl;
        // for(set<int>::iterator i1=trans.begin(); i1!=trans.end(); i1++){
        // 	cout<<*i1<<", ";
        // }
        // cout<<endl;
        // while(true){}

        set<int>::iterator it = trans.begin();
        greenWood->insertInTree(greenWood->root, trans, it);
		dbSize++;
   }
   // greenWood.printItOut();
   return greenWood;
}

void markPrefix(Node* n, bool reset, int activeFreq) {
	if (!(n->label==-1)) {
		if (reset) {
			n->isActive = true;
			n->activeFreq = activeFreq;
		} else {
			n->isActive = false;
			n->activeFreq = n->count;
		}
		markPrefix(n->parent, activeFreq, reset);
	}
}

// see if set not having cmp matter
void getFrequentSets(Tree* t, set<int> a, int level, 
int suppThresh, vector<set<int>>& minedItems, Node* curr){
	if (level==0) {
		// minedItems.push_back(a);
		return;
	}
	if (a.empty()) {
		int freq = 0;
		for (Node* n: t->pointerTable[level]) {
			freq += n->count;
		}
		if (freq>=suppThresh) {
			for (Node* n: t->pointerTable[level]) {
				markPrefix(n, true, freq);
				set<int> s;
				s.insert(n->label);
				getFrequentSets(t, s, --level, suppThresh, minedItems, n->parent);
				markPrefix(n, false, 0);
			}
		}
	} else {
		int freq = 0;
		for (Node* n: t->pointerTable[level]) {
			freq += n->count;
		}
		if (freq>=suppThresh) {
			set<int> s;
			s.insert(a.begin(), a.end());
			s.insert(curr->label);
			minedItems.push_back(s);
			getFrequentSets(t, s, --level, suppThresh, minedItems, curr->parent);
		}
	}
}

int main(int argc, char* argv[]){
	// argv[] = dataFile outFile percentageThresh
	ifstream dataFile;
	dataFile.open(argv[1]);
	getFlist(dataFile);

	int dbSize = 0;
	Tree* t = plantTree(dataFile, dbSize);
	int suppThresh = (atof(argv[3])*dbSize)/100;
	vector<set<int>> minedItemSets; 
	for (int i=t->sizeOfPointers-1; i>=0; i--) {
		set<int> s;
		getFrequentSets(t, s, i, suppThresh, minedItemSets, NULL);
	}
	dataFile.close();

	ofstream outFile;
	outFile.open(argv[2]);
	for (set<int> freqSet: minedItemSets) {
		for (auto it=freqSet.begin(); it!=freqSet.end(); it++) {
			cout << *it;
			if (it!=--freqSet.end()) {
				cout << " ";
			}
		}
		cout << endl;
	}

	return 0;
}