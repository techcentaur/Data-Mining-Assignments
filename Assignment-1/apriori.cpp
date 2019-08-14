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

set<set<int>> frequentSet1Gen(ifstream& dataFile, int percentageSuppThresh, int& totalTransactions) {

}

vector<set<set<int>>> aprioriAlgorithm(ifstream& dataFile, int percentageSuppThresh) {
    int totalTransactions;
    // for saving frequent sets, not saving their frequencies
    vector<set<set<int>>> listOfF;
    listOfF.push_back(frequentSet1Gen(dataFile, percentageSuppThresh, totalTransactions));
    set<set<int>>& lastF = listOfF[0];

    // loop check till Fk becomes empty
    while(!lastF.empty()) {
        // create pruned(check k-1 th set) candidates
        set<set<int>> candidates = candidateGeneration(lastF);
        // check thier frequencies
        set<pair<set<int>, int>, decltype(pcmp)> frequenciesOfFreqSet = 
        scanTransactionDB(dataFile, candidates);
        // remove infrequent
        for (auto setAndFreq: frequenciesOfFreqSet) {
            
        }
    }
}

int main(int argc, char* argv[]) {
    // argv[] = datafile outputfile support_threshold
    ifstream dataFile;
    dataFile.open(argv[1]);
    aprioriAlgorithm(dataFile, (int) argv[3]);
    return 0;
}
