## For GSPAN

- Edit the file path inside the file (I know :'( )
- Run `gspan.py`
- It'll create a new file in current directory

- Run the binary as:

NOTE: <support> -> frequency [0, 1] if 20% frequent -> 0.2 value should be put in support

`./gSpan-64 -f <filename> -s <support> -o -i`

- For more, read readme in gSpan-1 folder

## For GASTON

- Edit the file path inside the file (I know :'( )
- Run `gaston.py`
- It'll create a new file in current directory

- Run the binary as:

NOTE: support -> [0, 100]: 30 if 30% frequent graphs

`./gaston (support) (inputfile) (outfile)`

- For more, read readme in gaston folder

## For PAFI (FSG)

- Edit the file path inside the file (I know :'( )
- Run `pafi.py`
- It'll create a new file in current directory

- Run the binary as:

NOTE: support -> [0, 100]: 30 if 30% frequent graphs

`./fsg -s 100.0 -pt <inputfilename>`