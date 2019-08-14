// Implementing Apriori algorithm
#include<iostream>
#include<fstream>
#include<string>
using namespace std;

void AprioriAlgorithm(string dataFilePath){
	ifstream file;
	file.open(dataFilePath);
	int d;
	for(int i=0; i<156; i++){
	file>>d;
	cout<<d<<" "<<endl;
	}
	file.close();
}

int main(){
	string s;
	s="/home/solanki/Fall2019/COL761/Ass-1/webdocs.dat";
	AprioriAlgorithm(s);
	return 0;
}