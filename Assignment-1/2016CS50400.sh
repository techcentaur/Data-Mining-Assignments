if [ "$2" = "-plot" ]
then
   python3 plot.py "$1"
elif [ "$3" = "-apriori" ]
then
   g++ apriori.cpp
   ./a.out "$1" "${4}.txt" "$2"
elif [ "$3" = "-fptree" ]
then
   g++ fptree.cpp
   ./a.out "$1" "${4}.txt" "$2"
else
   echo "Unknown parameter!"
fi
