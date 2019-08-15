// Implementing Apriori algorithm

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <set>
#include <algorithm>
#include <unordered_map>

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

bool eqlFunc (const set<int>& a, const set<int>& b) {
    set<int>::iterator begin1 = a.begin();
    set<int>::iterator begin2 = b.begin();
    set<int>::iterator end1 = a.end();
    set<int>::iterator end2 = b.end();
    set<int>::iterator i1;
    set<int>::iterator i2;
    for (i1 = begin1, i2 = begin2; (i1 != end1) && (i2 != end2); ++i1, ++i2) {
        if (*i1 != *i2) {
            return false;
        }
    }
    return true;
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
vector<int> scanTransactionDB(ifstream& file, set<set<int>, cmp>& candidates) {
    vector<int> frequencies(candidates.size());
    file.clear();
    file.seekg(0, ios::beg);

    string line;
    while (getline(file, line)) {
        stringstream lineStream(line);
        set<int> items;
        int value;

        while (lineStream >> value) {
            items.insert(value);
        }
        int i = 0;
        for (set<int> c: candidates) {
            bool found = true;
            for (int item: c) {
                if (items.find(item) == items.end()) {
                    found = false;
                    break;
                }
            }
            if (found) { frequencies[i]++; }
            i++;
        }
    }
    return frequencies;
}

// Generates candidate sets of k length given frequent sets of k-1 length
set<set<int>, cmp> generateCandidates(set<set<int>, cmp>& frequentSets) {
    set<set<int>, cmp> candidateSets;
    int index = 0;
    set<set<int>>::iterator it1;
    set<set<int>>::iterator it2 = ++frequentSets.begin();

    for (it1 = frequentSets.begin(); it1 != frequentSets.end(); ++it1) {
        it2 = frequentSets.begin();
        advance(it2, index+1);
        while (it2 != frequentSets.end()) {
            set<int> s1 = *it1;
            set<int> s2 = *it2;
            set<int> s;
            bool flag = equal(s1.begin(), --s1.end(), s2.begin());
            if (!flag) {
                break;
            }
            int size = s1.size();
            for (auto& m: s1) { s.insert(m); }
            s.insert(*s2.rbegin());
            flag = true;
            for (set<int>::iterator k = s.begin(); k != s.end(); ++k) {
                set<int> scopy;
                for (auto& m: s) { 
                    if (m!=*k) { scopy.insert(m); }
                }
                bool found = false;
                for(auto& freq: frequentSets){
                    if(eqlFunc(freq, scopy)){
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    flag = false;
                }
            }
            if (flag) {
                candidateSets.insert(s);
            }
            ++it2;
        }
        index++;
    }
    return candidateSets;
}

set<set<int>, cmp> frequentSet1Gen(ifstream& dataFile, int percentageSuppThresh, int& totalTransactions) {
    unordered_map<int, int> freqMap;
    set<set<int>, cmp> f1;

    totalTransactions = 0;
    string line;
    while (getline(dataFile, line)) {
        stringstream lineStream(line);
        int itemId;

        while (lineStream >> itemId) {
            auto it = freqMap.find(itemId);
            if (it!=freqMap.end()) {
                it->second += 1;
            } else {
                freqMap.insert(make_pair(itemId, 1));
            }
        }
        totalTransactions++;
    }
    int suppThresh = (percentageSuppThresh*totalTransactions)/100;
    for (auto it=freqMap.begin(); it!=freqMap.end(); it++) {
        if (suppThresh <= it->second) {
            set<int> s;
            s.insert(it->first);
            // because set of set
            f1.insert(s);
        }
    }
    return f1;
}

vector<set<set<int>, cmp>> aprioriAlgorithm(ifstream& dataFile, float percentageSuppThresh) {
    int totalTransactions;
    // for saving frequent sets, not saving their frequencies
    vector<set<set<int>, cmp>> listOfF;
    listOfF.push_back(frequentSet1Gen(dataFile, percentageSuppThresh, totalTransactions));
    int suppThresh = (int) ((percentageSuppThresh * totalTransactions) / 100.0);

    int k = 0;
    // loop check till Fk becomes empty
    while(!listOfF[k].empty()) {
        // create pruned(check k-1 th set) candidates
        set<set<int>, cmp> candidates = generateCandidates(listOfF[k]);
        // check their frequencies
        vector<int> frequenciesOfFreqSet = scanTransactionDB(dataFile, candidates);
        // remove infrequent
        set<set<int>, cmp> afterPruning;
        int i = 0;
        for (auto& cand: candidates) {
            if (frequenciesOfFreqSet[i] >= suppThresh) {
                afterPruning.insert(cand);
            }
            i++;
        }
        listOfF.push_back(afterPruning);
        k++;
    }
    dataFile.close();
    return listOfF;
}

int main(int argc, char* argv[]) {
    // a.out datafile outputfile support
    ifstream dataFile;
    dataFile.open(argv[1]);
    vector<set<set<int>, cmp>> listOfF = aprioriAlgorithm(dataFile, atof(argv[3]));
    ofstream outFile;
    outFile.open(argv[2]);
    for (auto& f:listOfF) {
        for (auto& itemSets: f) {
            for (auto& item: itemSets) {
                outFile << item;
                if (item != *itemSets.rbegin()) {
                    outFile << " ";
                }
            }
            outFile << endl;
        }
    }
    outFile.close();
    return 0;
}
