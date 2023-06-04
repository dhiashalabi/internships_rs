# this script contains the functions for prepping the datasets for making recommendations


from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import numpy as np
import re

import nltk
nltk.download('punkt')
nltk.download('wordnet')

def tokenize(sentences):
    '''
    tokenizes a bunch of sentences after normalizing them and returns stemmed tokens.

    INPUT:
    sentences - a paragraph that need to be tokenized

    OUTPUT:
    tokens - list of stemmed tokens

    '''
    # normalizing, tokenizing, lemmatizing
    sentences = re.sub('\W', ' ', sentences) 
    sentences = re.sub('[0-9]', ' ', sentences)

    tokens = word_tokenize(sentences)
    tokens = [i.strip() for i in tokens]

    stemmer = PorterStemmer()
    tokens = [stemmer.stem(i) for i in tokens]
    return tokens


def similarity_matrix_wo_tfidf(df):
    '''
    returns a similarity matrix, in the form of a dataframe, between different internships by using the 
    details section

    INPUT:
    df - dataframe with 'details' as one of the columns

    OUTPUT:
    sim - similarity matrix(dataframe) with internship id as column and row labels 

    '''
    details = df['details']
    vect = CountVectorizer(tokenizer=tokenize, stop_words= 'english')

    mat = vect.fit_transform(details).toarray()
    sim = np.dot(mat, mat.T)
    sim = pd.DataFrame(sim, columns=df.id, index=df.id)
    return sim


def similarity_matrix_cat(df):
    '''
    returns a similarity matrix, in the form of a dataframe, between different internships by using the 
    title

    INPUT:
    df - dataframe with 'title' as one of the columns

    OUTPUT:
    sim - similarity matrix(dataframe) with internship id as column and row labels 
    '''
    cats = df['title']
    vect = CountVectorizer(tokenizer=tokenize, stop_words= 'english')
    tfidf = TfidfTransformer()

    mat = vect.fit_transform(cats).toarray()
    sim = np.dot(mat, mat.T)
    sim = pd.DataFrame(sim, columns=df.id, index=df.id)
    return sim

def return_sim(df):
    '''
    returns similarity dataframe and accepts clean dataframe
    '''
    sim_1 = similarity_matrix_wo_tfidf(df)
    sim_cat = similarity_matrix_cat(df)
    sim = sim_1 * 0.3 + sim_cat

    return sim
