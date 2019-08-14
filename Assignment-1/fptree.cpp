// FP-tree implementation

#include<iostream>
#include<fstream>
#include<vector>
#include<unordered_map>

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
    if(itemsMap[a] > itemsMap[b]) return true;
    else false;
}

class cmp{
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
			indexes[it.first] = i;
			i++; 
		}

		this->sizeOfPointers = i+1;
		pointerTable.reserve(this->sizeOfPointers);
	}

	void insertInTree(Node* root, set<int, cmp>& trans, set<int>::iterator i){
		if(i == trans.end()){return;}

		for(auto child: root->children){
			if(child->label == trans.at(i)){
				child->count += 1;
				insertInTree(child, trans, ++i);
				return;
			}
		}

		Node* newNode = new Node(trans.at(i), 1, root); // new Node: trans.at(i)->label, 1->freq, root->parent
		root->children.push_back(newNode);
		vector[this->indexes[trans.at(i)]].push_back(newNode); // put it in pointerTable
		
		insertInTree(newNode, trans, ++i);
		return;
	}
}

void plantTree(ifstream& file){
    string line;
    Tree greenWood;
    
    while (getline(file, line)){
        stringstream lineStream(line);
        set<int, cmp> trans;

        while (lineStream >> value){
            trans.insert(value)
        }

        set<int>::iterator it = trans.begin();
        greenWood.insertInTree(greenWood->root, trans, it);
   }
}

void getFrequentSets(Tree& t){

}

int main(){

}