## Name: Park Chang Whan
## Student ID: 1129623
## Part B Task 5
 
import re
import os
import argparse
import pandas as pd
import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import math
from numpy import dot
from numpy.linalg import norm

# Using argparse to find keywords to find matching
# At least one keyword to be inputted but can go beyond if user inputs more
parser = argparse.ArgumentParser(description='find all documents matching keywords given (Stemmer) and find cosine similarity')
parser.add_argument('keywords', type=str, metavar='', nargs = '+', help='all key words')
args = parser.parse_args()

def cosine_sim(v1, v2):
    """ 
    Get the cosine similarity score given query unit vector and document vector
    
    Returns cosine similarity score rounded up to 4 decimal places
    """
    
    # Pretty self-explanatory for equation of cosine similarity below
    return round(dot(v1, v2)/ (norm(v1)*norm(v2)),4)


def search_ranking(corpus, docID_corpus, stem_keys):
    """ 
    Get the ranking of matched documents by cosine similarity score
    
    Prints documentIDs matching all keywrods using Porter Stemmer method 
    with their corresponding cosine similarity scores (Descending order)
    """
    
    # Get matrix of token counts
    # Skip analyzer as already done into list of stemmed words
    vectorizer = CountVectorizer(analyzer=lambda word: word)
    token_counts = vectorizer.fit_transform(corpus).toarray()
    
    # Transform data to TF-IDF
    transformer = TfidfTransformer()
    docs_tfidf = transformer.fit_transform(token_counts).toarray()
    
    # Get the query(key) vector with the given vectorizer feature names already
    key_vector = vectorizer.transform([stem_keys]).toarray()[0]
    
    # Get unit vector for query(key) vector
    magnitude = math.sqrt(sum([x**2 for x in key_vector]))
    unit_key_vector = [x/magnitude for x in key_vector]
    
    # Find cosine similarity score for every document matched (round to 4 decimal places)
    sim_scores = [cosine_sim(unit_key_vector, docs_tfidf[doc_num]) for doc_num in range(docs_tfidf.shape[0])]
    
    # Add documentID and corresponding score to dataframe and print descending order of cosine sim scores
    doc_sim_df = pd.DataFrame({'documentID': docID_corpus, 'score': sim_scores})
    print(doc_sim_df.sort_values('score', ascending = False).to_string(index=False))

    
def stemmer_search(keys):
    """
    Use Porter Stemmer on texts in documents and keywords, and find all documents containing all the stemmed keywords
    
    Returns - list of stemmed words of each documents containing all keywords using Porter Stemmer method
            - list of correspoding documentIDs to each stemmed words in order of stemmed words list
            - list of stemmed keys
    """
    
    porterStemmer = PorterStemmer()
    articles_df = pd.read_csv('partb1.csv', encoding = 'ISO-8859-1')
    corpus = []
    docID_corpus = []
    
    # Use Porter Stemmer on keywords (include duplicates for search rankings)
    stem_keys = []
    for word in keys:
        s_word = porterStemmer.stem(word)
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
            
            # Use Porter Stemmer on text (include duplicates for search rankings)
            stem_words = []
            for word in words:
                s_word = porterStemmer.stem(word)
                stem_words.append(s_word)

            # Check for every keyword in text case insensitive
            # if at least one keyword is missing from text, get out and go to next file
            for keyword in stem_keys:
                if keyword not in stem_words:
                    match = False
                    break
                        
        else:
            match = False
           
        # If all keywords present, get the vector counts to find TF-IDF to find cosine similarity
        if match:
            corpus.append(stem_words)
            docID_corpus.append(articles_df.loc[articles_df['filename'] == filename, ['documentID']].to_string(index=False, header = False))
        
    return(corpus, docID_corpus, stem_keys)
            
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
    
    # Get documentIDs and stemmed words of documents containing all stemmed keywords
    corpus, docID_corpus, stem_keys = stemmer_search(args.keywords)
    
    # Get ranking of matched documents using cosine similarity scores
    search_ranking(corpus, docID_corpus, stem_keys)
