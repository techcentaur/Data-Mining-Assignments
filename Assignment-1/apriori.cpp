// Implementing Apriori algorithm

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <set>
#include <algorithm>

using namespace std;


bool cmpFunc (const set<int>& a, const set<int>& b) {
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

struct pcmp {
    bool operator() (const pair<set<int>, int>& a, const pair<set<int>, int>& b) const {
        return cmpFunc(a.first, b.first);
    }
};

struct cmp {
    bool operator() (const set<int>& a, const set<int>& b) const {
        return cmpFunc(a, b);
    }
    set<set<int>> s;
};


// Takes candidate set as input, scans the whole transaction database, and returns frequencies
set<pair<set<int>, int>, pcmp> scanTransactionDB(ifstream& file, set<set<int>>& candidates) {
    set<pair<set<int>, int>, pcmp> frequencies;
    
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

// // Generates candidate sets of k length given frequent sets of k-1 length
set<set<int>> candidateGeneration(set<set<int>>& frequentSets) {
    set<set<int>, cmp> candidateSets;

    for (set<set<int>>::iterator i = frequentSets.begin(); i != --frequentSets.end(); ++i) {
        set<int> s1 = *i;
        set<set<int>>::iterator j = i;
        set<int> s2 = *(++j);

        set<int> s;
        bool flag = true;

        set<int>::iterator begin1 = s1.begin();
        set<int>::iterator begin2 = s2.begin();
        set<int>::iterator end1 = s1.end();
        set<int>::iterator end2 = s2.end();
        set<int>::iterator i1;
        set<int>::iterator i2;
        for (i1 = begin1, i2 = begin2; (i1 != end1) && (i2 != end2); ++i1, ++i2) {
            if (*i1 != *i2) {
                flag = false;
                break;
            }
        }
        // flag = includes(s1.begin(), --s1.end(), s2.begin(), --s2.end());
        if (!flag) { continue; }

        int size = s1.size();
        copy(s1.begin(), s1.end(), s.begin());
        s.insert(*s2.rbegin());

        // bool flag = false
        // for (auto f: frequentSets) {

        // }
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
