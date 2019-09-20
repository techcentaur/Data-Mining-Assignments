## All the files we bundled

- `compile.sh`: File is empty | Nothing to compile.
- `gaston.py`: Convert graphs in given format to the format accepted by the gaston binary.
- `pafi.py`: Convert graphs in given format to the format accepted by the pafi binary.
- `gSpan.py`: Convert graphs in given format to the format accepted by the gSpan binary.

- `plot.py`: Plots, running times, for different algorithms for different support levels.
- `plot.sh`: Bash script which calls plot.py

- `index_and_query.py`: Code of part-2 | Implements an optimized version of subgraph isomorphism.
- `index_and_query.sh`: Calls the `index_and_query.py` file

- `Readme.txt`: Contains report of the assignment

Directories:
- `gSpan-1`: Contains gSpan executable
- `gaston-1.1`: Contains the code and binary of gaston 
- `pafi-1.0.1`: Contains the contents of binary of PAFI


## Explanation for Part-1

1. Plot the running times
unit in seconds
{
'gSpan': [3.0882132053375244, 5.549440860748291, 47.2048282623291, 263.76826000213623, 771.7448644638062], 

'PAFI': [22.782464504241943, 128.17044353485107, 372.22339129447937, 1312.6531813144684, 3962.968509197235]
}

We could not run the benchmark script for gaston, because it was taking too much time and we were very close to deadline. But, we did run gaston on a dataset of 1000 graphs, and it was running quite fast, faster than the other two algorthims.

2. Explain the trend and comment on growth rates (why one technique is faster than others)

PAFI is much slower than gSpan: This is because it generates all the candidates of k edges before finding out the frequent patterns of k-edge. This takes very high amount of time.

Whereas gSpan does edge-extension to only those graphs which are frequent, and with its min DFS code technique, it performs subgraph isomorphism much faster than PAFI.


The trend, as in the running times observed, occurs similar to the reasoning.

More support takes less time, as more support implies that a particular graph would be frequent only if it is occuring in more number of database graphs, this directly implies less further candidates to explore. Such a trend can be seen in either of the PAFI or gSpan running times over the support from 95 to 5, where it takes less time in 95% support and keep on increasing as we lower the support.



## Approach for Part-2

We did not fix a value for m, rather than that we concluded that fixing a value for support (an adequately higher one,) whilst mining frequent patterns will get us small number of frequent subgraphs that we can assume to be our feature patterns. So here is how we answer this questions:

1. What should be the value of m?
- Support should be 72%, and so the value of m would be the number of frequent patterns with this support.

2. How do you mine the subgraph patterns?
- We mine the subgraph patterns by using the binary for PAFI, we wanted to use gSpan binary as it is way faster than PAFI, but the output of gSpan was not indicating in which of the database transactions the mined frequent pattern is present in, which was a crucial information for us, hence we took the high way, and used PAFI as our algorithm to mine the frequent subgraphs.

3. How do you prune the frequent subgraphs to m?
- By fixing a particular value of support: We experimented with several support values, and we came to see that a support of 72.0 works best in our favour.


## Names, Entry numbers, and Individual Contributions

2016CS50400
Sumit Ghosh
- Ran part-1, part-2, and all plotting on HPC, and written all the required scripts for submission and dealt with the subsequent problems
- Worked in the code and discussion of part-2

2016CS50401
Ankit Solanki
- Found the binaries and wrote the format conversion scripts
- Worked in the code and discussion for part-2

2016CS50403
Yash Malviya
- Worked in major portion in the code and discussion for part-2
- And debugging of the scripts


