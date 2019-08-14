// Implementing Apriori algorithm

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <set>
#include <algorithm>

using namespace std;

bool cmp(set<int>& a, set<int>& b) {
    set<int>::iterator begin1 = a.begin();
    set<int>::iterator begin2 = b.begin();
    set<int>::iterator end1 = a.end();
    set<int>::iterator end2 = b.end();
    set<int>::iterator i1;
    set<int>::iterator i2;
    for (i1 = begin1, i2 = begin2; (i1 != end1) && (i2 != end2); ++i1, ++i2) {
        if (*i1 < *i2) {
            return true;
        }
    }
    return false;
}

bool pcmp(pair<set<int>, int>& a, pair<set<int>, int>& b) {
    return cmp(a.first, b.first);
}

// Takes candidate set as input, scans the whole transaction database, and returns frequencies
set<pair<set<int>, int>, decltype(pcmp)> scanTransactionDB(ifstream& file, set<set<int>>& candidates) {
    set<pair<set<int>, int>, decltype(pcmp)> frequencies;
    
    for (auto c: candidates) {
        frequencies.insert(make_pair(c, 0));
    }

    string line;
    while (getline(file, line)) {
        stringstream lineStream(line);
        set<int> items;
        int value;

        while (lineStream >> value) {
            items.insert(value);
        }

        for (auto f: frequencies) {
            bool found = true;
            for (int item: f.first) {
                if (items.find(item) == items.end()) {
                    found = false;
                    break;
                }
            }
            if (found) {
                f.second++;
            }
        }
    }
    return frequencies;
};

// Generates candidate sets of k length given frequent sets of k-1 length
set<set<int>> candidateGeneration(set<set<int>>& frequentSets) {
    vector <set<int>> candidateSets;

    for (int i = 0; i < frequentSets.size() - 1; i++) {
        set<int> s;
        for (i1 = begin1; i1 != end1; ++i1)

        flag = includes(frequentSets[i].begin(), frequentSets[i].end(), frequentSets[i+1].begin(), frequentSets[i+1].end());
        if (*frequentSets[i].rbegin() != *frequentSets[i+1].rbegin()) { continue; };

        int size = frequentSets[i + 1].size();
        copy(frequentSets[i + 1].begin(), frequentSets[i + 1].end(), s.begin());
        s.insert(*frequentSets[i + 1].rbegin());

        bool flag = false
        for (auto f: frequentSets) {

        }
    }
}

//void AprioriAlgorithm(string dataFilePath) {
//    ifstream file;
//    file.open(dataFilePath);
//
//    std::string line;
//    while (std::getline(file, line)) {
//        std::vector<int> lineInts;
//        std::stringstream lineStream(line);
//
//        int value;
//        while (lineStream >> value) {
//            // Add the integers from a line to a 1D array (vector)
//            lineInts.push_back(value);
//        }
//        // When all the integers have been read, add the 1D array
//        // into a 2D array (as one line in the 2D array)
//        data.push_back(lineData);
//    }
//
//    int d;
//    for (int i = 0; i < 156; i++) {
//        file >> d;
//        cout << d << " " << endl;
//    }
//    file.close();
//}

//int main() {
//    string s;
//    s = "/home/solanki/Fall2019/COL761/Ass-1/webdocs.dat";
//    AprioriAlgorithm(s);
//    return 0;
//}
