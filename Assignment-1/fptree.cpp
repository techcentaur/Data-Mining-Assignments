// FP-tree implementation

#include<iostream>
#include<fstream>
#include<vector>
#include<unordered_map>

struct Node{
	int count;
	int label;
	vector<Node*> children;

	Node(int l, int c){
		this->label = l;
		this->count = c;
	}
};

unordered_map<int, int> itmesMap;

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

struct LinkNode{
	int label;
	Node* firstLink;
	Node* lastLink;
	LinkNode(int l, Node* fl, Node* ll){
		this->label = l;
		this->firstLink = fl;
		this->lastLink = ll;
	}
};

class Tree{
public:
	Node* root;
	unordered_map<int, LinkNode> pointersTo;

	Tree(){
		this->root = new Node(-1, -1); // NULL node
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

		Node* newNode = new Node(trans.at(i), 1);
		root->children.push_back(newNode);
		
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

int main(){

}