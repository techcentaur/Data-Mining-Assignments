#!/bin/bash

if [ "$2" = "-plot" ]
then
   python3 plot.py "$1"
elif [ "$3" = "-apriori" ]
then
   ./apriori "$1" "${4}.txt" "$2"
elif [ "$3" = "-fptree" ]
then
   ./fptree "$1" "${4}.txt" "$2"
else
   echo "Unknown parameter!"
fi
