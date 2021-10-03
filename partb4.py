## Name: Park Chang Whan
## Student ID: 1129623
## Part B Task 4

import re
import pandas as pd
import nltk
import os
import argparse
from nltk.stem.porter import *


# Using argparse to find keywords to find matching
# At least one keyword to be inputted but can go beyond if user inputs more
parser = argparse.ArgumentParser(description='find all documents matching keywords given (Stemmer)')
parser.add_argument('keywords', type=str, metavar='', nargs = '+', help='all key words')
args = parser.parse_args()


def stemmer_search(keys):
    """
    Use Porter Stemmer on texts in documents and keywords, and find all documents containing all the stemmed keywords
    
    Prints all documentIDs of documents containing all keywords using the Porter Stemmer method
    """
    
    porterStemmer = PorterStemmer()
    articles_df = pd.read_csv('partb1.csv', encoding = 'ISO-8859-1')
    
    # Use Porter Stemmer on keywords
    stem_keys = []
    for word in keys:
        s_word = porterStemmer.stem(word)
        if s_word not in stem_keys : 
            stem_keys.append(s_word.lower())
            
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
            
            # Use Porter Stemmer on text
            stem_words = []
            for word in words:
                s_word = porterStemmer.stem(word)
                if s_word not in stem_words : 
                    stem_words.append(s_word)

            # Check for every keyword in text case insensitive
            # if at least one keyword is missing from text, get out and go to next file
            for keyword in stem_keys:
                if keyword not in stem_words:
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
    
    # Find all documentIDs of documents containing all the keywords using Porter Stemmer method
    stemmer_search(args.keywords)
