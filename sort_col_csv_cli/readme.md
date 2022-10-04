# Simple dataframe column sorting script

This script allows you to sort a dataframe read from a raw text file with a specific column separator or from a pickle file by a desired column in either ascending or descending order.

It's a simple CLI tool, the usage is described with the `-h` or `--help` flags:

```
usage: sort_cols.py [-h] [-is INPUT_SEPARATOR] [-os OUTPUT_SEPARATOR] [-c COLUMN] [-d] [-o OUTPUT] input_file

Sort rows in a file containing a dataframe by a specific column

positional arguments:
  input_file            Input file containing a dataframe. 
                        Default: csv, Supported: plain-text files with arbitrary separator `sep`, pickle

optional arguments:
  -h, --help            show this help message and exit
  -is INPUT_SEPARATOR, --input-separator INPUT_SEPARATOR
                        Separator for the input file. 
                        Default: ,
  -os OUTPUT_SEPARATOR, --output-separator OUTPUT_SEPARATOR
                        Separator for the output file. 
                        Default: ,
  -c COLUMN, --column COLUMN
                        Column to order by. 
                        Default: column
  -d, --descending      Sort in descending order. 
                        Default: False
  -o OUTPUT, --output OUTPUT
                        Output filename. 
                        Default: same file name as input file
```
