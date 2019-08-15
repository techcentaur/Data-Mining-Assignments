Files bundled are;

1. apriori.cpp: Source code for apriori algorithm
2. fptree.cpp: Source code for FP-tree algorithm
3. install.sh: installation script that clones the repo and loads hpc modules
4. compile.sh: script that compiles source files
5. 2016CS50400.sh: script that runs the algorithms.
6. plot.py: the python script used to generate plot.


Explanation of part b;

We can see from the graph that for large input database size and low threshold, the apriori algorithms performs poorly compared to fptree algorithm. The suspected reasons being
1. In fptree, the transaction db is scanned only twice: at the time of the initial frequency count (flist) and at the time of the tree consruction. Whereas in case of apriori, the database is scanned k times, as long as the set of frequents set doesn't become empty.
2. Also, in apriori, much greater space is used. This contributes to the running time too.

We can conclude, that the DFS-like fptree algorithm is much more efficient that BFS-like apriori algorithm.



Assignment submitted by;

1. Sumit Kumar Ghosh, 2016CS50400
2. Ankit Solanki, 2016CS50401
3. Yash Malviya, 2016CS50403
