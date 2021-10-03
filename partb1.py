## Name: Park Chang Whan
## Student ID: 1129623
## Part B Task 1

import re
import pandas as pd
import os
import argparse

# Using argparse to find name to output CSV File to
parser = argparse.ArgumentParser(description='Get list of all document IDs')
parser.add_argument('file_name', type=str, metavar='', help='Name of output file for document ID lists')
args = parser.parse_args()

def pattern_search(name):
    """
    Get every documentID of each file in 'cricket'
    
    Output the filename with corresponding documentID in CSV file called 'name'
    """
    
    # Get pattern to find Document IDs
    # '[A-Z]{4}' --> 4 consecutive capital letters
    # '-' --> dash
    # '\d{3}' --> 3 consecutive digits
    # '([A-Z]((?=[^a-z])|$))?' --> Capital letter at the end OR
    #                              followed by anything other than lowercase letters
    pattern = r'[A-Z]{4}-\d{3}([A-Z]((?=[^a-z])|$))?'

    document_set = pd.DataFrame(columns = ['filename', 'documentID'])
    
    # Iterate through every file in 'cricket'
    for filename in os.listdir('cricket'):
        if filename.endswith(".txt"):
            file = open('cricket/'+filename, 'r')
            text = file.read()
            
            # Search for the matching pattern in text
            matched = re.search(pattern, text).group()
            
            # Collate the filename and matched pattern into 'document_set'
            file_data = [{'filename':filename , 'documentID':matched}]
            document_set = document_set.append(file_data, ignore_index=True)
    
    document_set = document_set.sort_values(by=['filename'])
    
    # Save new dataframe to CSV file given 'name'
    document_set.to_csv(name, index=False)
    
    
    
    
if __name__ == '__main__':
    
    # Find documentID in text for every file in 'cricket'
    pattern_search(args.file_name)
