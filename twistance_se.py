import pandas as pd
import re, time, sys, math, csv, operator
from nltk.corpus import stopwords
import numpy as np
from nltk.stem.porter import *
from collections import Counter,defaultdict

'''
__________METRICS KEY__________

doc_lengths = list of tweet lengths
docLengthAvg = average length of tweet
QF = Query Frequency Counter Object
CF = Collection Frequency Counter Object
DFs = List of individual tweet counters
docN = Number of tweets in the collection
'''


### DATA ###
tweets_df = pd.read_csv('tweets.csv',error_bad_lines=False, encoding='latin-1',sep=',')


def preprocess_text(raw_text,lower=True, use_stemmer=True, remove_stop=True, remove_ints=True, length_min=0, length_max=15):
    '''PREPROCESSES A TWEET'''

    try:
        raw_text = raw_text.encode('utf-8')
    except:
        raw_text = str(raw_text)

    #PREPROCESSING: LOWERCASE
    if lower == True:
        text = raw_text.lower()
    else:
        text = raw_text
    tokens = re.findall(r"(\w+)", text)

    #PREPROCESSING: REMOVE STOP WORDS
    stop = set(stopwords.words('english'))
    if remove_stop == True:

        tokens = [token for token in tokens if token not in stop]
    else:
        pass

    # PREPROCESSING: STEM WORDS
    stemmer = PorterStemmer()
    if use_stemmer == True:
        tokens = [stemmer.stem(token) for token in tokens]
    else:
        pass

    # PREPROCESSING: REMOVE INTEGERS
    if remove_ints == True:
        for token in tokens:
            try:
                int(token)
                tokens.remove(token)
            except:
                pass

    # PREPROCESSING: LENGTH RESRICTIONS
    tokens = [token for token in tokens if len(token) > length_min]
    tokens = [token for token in tokens if len(token) < length_max]
    return tokens


def flatten_list(list_of_lists):
    '''FLATTENS A LIST OF LISTS'''
    return [item for sublist in list_of_lists for item in sublist]


def create_collection_frequency(dataframe, tweet_column):
    '''CREATES A DICTIONARY WITH UNIGRAM COUNTS IN THE ENTIRE TWEET COLLECTION'''
    print "Counting Unigrams in all tweet collection..."
    unigram_collection_counter = Counter()
    list_of_raw_tweets = []
    for index, row in dataframe.iterrows():
        list_of_raw_tweets.append(row[tweet_column])
        tokens = preprocess_text(row[tweet_column])
        for token in tokens:
            unigram_collection_counter[token] += 1
    return unigram_collection_counter, list_of_raw_tweets

def create_query_frequency(query):
    '''CREATES A DICTIONARY WITH TERM COUNTS IN QUERY'''
    query_frequency_counter = Counter()
    processed_query = preprocess_text(query)
    for term in processed_query:
        query_frequency_counter[term] += 1
    return query_frequency_counter

def create_document_frequencies(dataframe,tweet_column):
    '''CREATES A LIST OF DICTIONARS WITH TERM COUNTS IN EACH TWEET'''
    counter_list =[]
    for index, row in dataframe.iterrows():
        document_frequency_counter = Counter()
        tokens = preprocess_text(row[tweet_column])
        for token in tokens:
            document_frequency_counter[token] += 1
        counter_list.append(document_frequency_counter)
    return counter_list

def calc_tweet_lengths(dataframe, tweet_column):
    '''CREATES A LIST OF TWEET LENGTHS AND CALCULATES AVG TWEET LENGTH'''
    tweet_lengths = []
    for index, row in dataframe.iterrows():
        tokens = preprocess_text(row[tweet_column])
        tweet_lengths.append(len(tokens))
    total_num_tokens = sum(tweet_lengths)
    avg_tweet_length = float(total_num_tokens) / len(tweet_lengths)
    number_tweets = len(tweet_lengths)
    return tweet_lengths, avg_tweet_length, number_tweets

def debugging_one(DFs,doc_lengths):
    if len(DFs) != len(doc_lengths):
        print "SIZE MISMATCH"
    else:
        print "All Clear"

def implement_bm25(dataframe, tweet_column, query, docN, DFs, doc_lengths,docLengthAvg, QF, CF):
    '''SCORES EACH TWEET BASED ON QUERY'''
    print "Conducting Search...Scoring tweets..."
    scores = defaultdict(float)
    okapiK1 = 1.0
    okapiB = 0.2
    okapiK3 = 1000
    processed_query = preprocess_text(query)
    for index, row in dataframe.iterrows():
        scores[index] = 0
        tweet_tokens = preprocess_text(row[tweet_column])
        for term in processed_query:
            try:
                idf = math.log((docN-CF[term]+0.5)/CF[term]+0.5)
                weight = ((okapiK1+1.0)*DFs[index][term]) / (okapiK1*(1.0-okapiB+okapiB*doc_lengths[index]/docLengthAvg)+ DFs[index][term])
                tweight = ((okapiK3+1)*QF[term])/(okapiK3+QF[term])
                scores[index] += idf*weight*tweight
            except:
                scores[index] += 0
    return scores

def retrieve_top_n_tweets(top_result_indexes):
    num_results = raw_input("Search Complete! How many results do you want?: ")
    top_result_indexes = dict(sorted(top_result_indexes.iteritems(), key=operator.itemgetter(1), reverse=True)[:int(num_results)]).keys()
    for result_index in top_result_indexes:
        print list_of_raw_tweets[result_index] +'\n'

if __name__=='__main__':
    
    query = raw_input("Please enter your search query: ")
    if query.lower() == "i'm done":
        running = False
    else:
        running = True
    while running:
        QF = create_query_frequency(query)
        CF, list_of_raw_tweets = create_collection_frequency(tweets_df,'Tweet')
        DFs = create_document_frequencies(tweets_df,'Tweet')
        doc_lengths, docLengthAvg, docN = calc_tweet_lengths(tweets_df,'Tweet')
        debugging_one(DFs,doc_lengths)

        bm25_scores = implement_bm25(tweets_df, 'Tweet', query, docN, DFs, doc_lengths, docLengthAvg, QF, CF)
        retrieve_top_n_tweets(bm25_scores, tweets_df)
        query = raw_input("Please enter your search query: ")
        if query.lower() == "i'm done":
            running = False
        else:
            running = True
