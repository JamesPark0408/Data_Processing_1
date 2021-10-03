## Name: Park Chang Whan
## Student ID: 1129623
## Part B Task 2

import re
import argparse

# Using argparse to find name to output CSV File to
parser = argparse.ArgumentParser(description='Preprocess text in given file')
parser.add_argument('file_name', type=str, metavar='', help='Name of file for preprocessing')
args = parser.parse_args()

def preprocess(name):
    """
    Preprocess given the file 'name' according to:
    1) Remove all non-alphabetic characters except for spacing characters (whitespace, tabs, newlines)
    2) Convert all spacing characters to whitespace and 
        ensure that only one whitespace character exists between each word
    3) Change all uppercase characters to lowercase
    
    Prints preprocessed text in given file 'name'
    """
    
    # Read file of given 'name'
    file = open(name[:7] + '/' + name[7:], 'r')
    text = file.read()
    
    # Do number (1) of preprocess
    pattern1 = r'[^a-zA-Z\s]'
    revised_text_1 = re.sub(pattern1, '', text)
    
    # Do number (2) of preprocess
    pattern2 = r'\s+'
    revised_text_2 = re.sub(pattern2, ' ', revised_text_1)
    
    # Do number (3) of preprocess and print result
    print(revised_text_2.lower())
     
        
if __name__ == '__main__':
    
    # Preprocess text in given 'file_name'
    preprocess(args.file_name)
