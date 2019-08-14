// Implementing Apriori algorithm

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

// Takes candidate set as input, scans the whole transaction database, and returns frequencies
vector <pair<int, int>> scanTransactionDB(ifstream file, vector <set<int>> &candidates) {
    vector < pair < set < int > , int >> frequencies;
    for (auto c: candidates) {
        frequencies.push_back(make_pair(c, 0));
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
                if (items.find(element) == items.end()) {
                    found = false;
                    break;
                }
            }
            if (found) {
                f.second++;
            }
        }
    }
    return frequecies;
};

// Generates candidate sets of k length given frequent sets of k-1 length
vector <set<int>> candidateGeneration(vector <set<int>> &frequentSets) {
    vector <set<int>> candidateSets;

    for (int i = 0; i < frequentSets.size() - 1; i++) {
        set<int> s;
        bool flag = true;

        for (int k = 0; k < frequentSets[i].size() - 1; k++) {
            if (frequentSets[i][k] != frequentSets[i + 1][k]) {
                flag = false;
                break;
            }
        }
        if (!flag) { continue; }

        int size = frequentSets[i + 1].size();
        copy(frequentSets[i + 1].begin(), frequentSets[i + 1].end(), s.begin());
        s.insert(frequentSets[i + 1][size - 1]);

        for (
    }
}

void AprioriAlgorithm(string dataFilePath) {
    ifstream file;
    file.open(dataFilePath);

    std::string line;
    while (std::getline(file, line)) {
        std::vector<int> lineInts;
        std::stringstream lineStream(line);

        int value;
        while (lineStream >> value) {
            // Add the integers from a line to a 1D array (vector)
            lineInts.push_back(value);
        }
        // When all the integers have been read, add the 1D array
        // into a 2D array (as one line in the 2D array)
        data.push_back(lineData);
    }

    int d;
    for (int i = 0; i < 156; i++) {
        file >> d;
        cout << d << " " << endl;
    }
    file.close();
}

int main() {
    string s;
    s = "/home/solanki/Fall2019/COL761/Ass-1/webdocs.dat";
    AprioriAlgorithm(s);
    return 0;
}
