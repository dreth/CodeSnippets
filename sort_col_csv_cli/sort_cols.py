import argparse
from operator import index
from random import random
import pandas as pd
import numpy as np

# parse cli arguments
parser = argparse.ArgumentParser(description="Sort rows in a file containing a dataframe by a specific column", formatter_class=argparse.RawTextHelpFormatter)

# input filename argument
parser.add_argument("input_file", help="Input file containing a dataframe. \nDefault: csv, Supported: plain-text files with arbitrary separator `sep`, pickle")

# input separator argument
parser.add_argument("-is", "--input-separator", type=str, default=",", help="Separator for the input file. \nDefault: ,")

# output separator argument
parser.add_argument("-os", "--output-separator", type=str, default=",", help="Separator for the output file. \nDefault: ,")

# column to order by argument
parser.add_argument("-c", "--column", type=str, default="column", help="Column to order by. \nDefault: column")

# descending or ascending
parser.add_argument("-d", "--descending", action="store_true", help="Sort in descending order. \nDefault: False")

# output filename argument
random_value = ''.join([str(np.random.randint(10)) for _ in range(50)])
parser.add_argument("-o", "--output", type=str, default=random_value, help="Output filename. \nDefault: same file name as input file")

# parse arguments
args = parser.parse_args()

# check args
def load_input_file():
    # check that the file has an extension
    if '.' not in args.input_file:
        raise ValueError("Input file must have an extension")
    
    # if it does, read it and return it
    else:
        # check if it's a plaintext file
        try:
            df = pd.read_csv(args.input_file, sep=args.input_separator, index_col=False)
            if 'Unnamed: 0' in df.columns:
                return df.drop('Unnamed: 0', axis=1)
            else:
                return df
        except:
            pass

        # check if it's a pickle file
        try:
            return pd.read_pickle(args.input_file)
        except:
            raise ValueError("Input file must be a csv or pickle file") from args.input_file


# order data by a column
def order_data(df):
    return df.sort_values(by=args.column, ascending=not args.descending)

# output file
def output_file(df):
    # check if the output file has an extension
    if '.' not in args.output:
        raise ValueError("Output file must have an extension")

    # if it does, write it
    else:
        # set original name if no name was chosen
        args.output = args.input_file if args.output == random_value else args.output

        # check if it's a pickle file
        try:
            pd.read_pickle(args.input_file)
            df.to_pickle(args.output)
            return
        except:
            pass

        try:
            df.to_csv(args.output, sep=args.output_separator, index=False)
            return
        except:
            raise ValueError("Output file must be a csv or pickle file") from args.output

# output the file
output_file(order_data(load_input_file()))
