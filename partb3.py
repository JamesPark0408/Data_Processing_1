## Name: Park Chang Whan
## Student ID: 1129623
## Part B Task 3

import re
import pandas as pd
import nltk
import os
import argparse

# Using argparse to find keywords to find matching
# At least one keyword to be inputted but can go beyond if user inputs more
parser = argparse.ArgumentParser(description='Find all documents matching keywords given')
parser.add_argument('keywords', type=str, metavar='', nargs = '+', help='all keywords')
args = parser.parse_args()

def basic_search(keys):
    """
    Search for all documents containing all the keywords
    
    Prints all documentIDs of documents containing all keywords
    """
    
    articles_df = pd.read_csv('partb1.csv', encoding = 'ISO-8859-1')
    
    # Iterate through every file in 'cricket'
    for filename in os.listdir('cricket'):
        
        match = True
        
        # Get text from file and match
        if filename.endswith(".txt"):
            file = open('cricket/'+filename, 'r')
            text = file.read()
            
            # Preprocess text first
            p_text = preprocess(text)
            
            # Tokenize text      
            words = nltk.word_tokenize(p_text)
            
            # Check for every keyword in text case insensitive
            # if at least one keyword is missing from text, get out and go to next file
            for keyword in keys:
                if keyword.lower() not in words:
                    match = False
                    break
                        
        else:
            match = False
           
        # If all keywords present, print it out
        if match:
            print(articles_df.loc[articles_df['filename'] == filename, ['documentID']].to_string(index=False, header = False))
           
        
def preprocess(text):
    """
    1) Remove all non-alphabetic characters except for spacing characters 
       (whitespace, tabs, newlines)
    2) Convert all spacing characters to whitespace and 
       ensure that only one whitespace character exists between each word
    3) Change all uppercase characters to lowercase
    
    Returns preprocessed text in given file 'name'
    """        
    
    # Do number (1) of preprocess
    pattern1 = r'[^a-zA-Z\s]'
    revised_text_1 = re.sub(pattern1, '', text)
    
    # Do number (2) of preprocess
    pattern2 = r'\s+'
    revised_text_2 = re.sub(pattern2, ' ', revised_text_1)
    
    # Do number (3) of preprocess and return  
    return(revised_text_2.lower())
               

if __name__ == '__main__':
    
    # Find all documentIDs of documents containing all the keywords
    basic_search(args.keywords)
