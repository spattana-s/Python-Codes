
# coding: utf-8

# # Assignment 5: Natural Language Processing - Collocations and TF-IDF 

# ## 1.  collocations
# - Define a function top_collocation(tokens, K) to find top-K collocations in specific patterns in a document as follows:
#   - takes a list of tokens and K as inputs
#   - uses the following steps to find collocations:
#     - POS tag each token
#     - create bigrams
#     - get frequency of each bigram (you can use nltk.FreqDist)
#     - keep only bigrams matching the following patterns:
#        - Adj + Noun: e.g. linear function
#        - Noun + Noun: e.g. regression coefficient
#   - returns top K collocations by frequency

# ## 2. Document search by TF-IDF
# 
# 1. Modify tfidf and get_doc_tokens functions in Section 7.5 of your lecture notes to add “normalize” as a parameter. This parameter can take two possible values: None, "stem". The default value is None; if this parameter is set to "stem", stem each token. 
# 2. In the main block, do the following:
#     1. Read the dataset “amazon_review_300.csv”. This dataset has 3 columns: label, title, review. We’ll use “review” column only in this assignment.
#     2. Calculate the tf-idf matrix for all the reviews using the modified functions tfidf function, each time with a different “normalize” value 
#     3. Take any review from your dataset, for each "normalize" option, find the top 5 documents most similar to the selected review, and print out these reviews
#     4. Check if the top 5 reviews change under different "normalize" options. Which option do you think works better for the search? Write down your analysis as a print-out, or attach a txt file if you wish.
#     5. (**bouns**) For each pair of similar reviews you find in (C), e.g. review x is similar to review y, find matched words under each "normalize" option. Print out top 10 words contributing most to their cosine similarity. (Hint: you need to modify the tfidf function to return the set of words as a vocabulary)

# In[65]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import nltk
from nltk.collocations import *

def top_collocation(tokens, K):
    result=[]
    

    tokens=nltk.word_tokenize(tokens)

    # tag each tokenized word
    tagged_tokens= nltk.pos_tag(tokens)

    bigrams=list(nltk.bigrams(tagged_tokens))

    word_dist=nltk.FreqDist(bigrams)


    phrases=[ (x[0],y[0]) for (x,y) in bigrams              if (x[1].startswith('JJ')              and y[1].startswith('NN')) or              (x[1].startswith('NN')              and y[1].startswith('NN'))]


    phrases_dist=nltk.FreqDist(phrases)

    result=phrases_dist.most_common(K)
    
    
    return result

tokens= nltk.corpus.reuters.raw('test/14826')
top_collocation(tokens, 10)


# modify these two functions
def get_doc_tokens(doc):
 
    return None

def tfidf(docs):
    
    return None
            


# In[ ]:


import nltk
import csv

if __name__ == "__main__":  
    
    # test collocation
    text=nltk.corpus.reuters.raw('test/14826')
    tokens=nltk.word_tokenize(text.lower())
    print(top_collocation(tokens, 10))
    
    
    # load data
    docs=[]
    with open("../dataset/amazon_review_300.csv","r") as f:
        reader=csv.reader(f)
        for line in reader:
            docs.append(line[2])
    
    # Find similar documents -- No STEMMING
    
    # Find similar documents -- STEMMING  


# In[9]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import nltk, re, string
from sklearn.preprocessing import normalize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import csv
from scipy.spatial import distance
stop_words = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

def get_doc_tokens(doc, normalize_None_or_Stem="Stem"):
    stop_words = stopwords.words('english')
    if normalize_None_or_Stem=="None":
        tokens = [token.strip()               for token in nltk.word_tokenize(doc.lower())               if token.strip() not in stop_words and               token.strip() not in string.punctuation]
        token_count={token:tokens.count(token) for token in set(tokens)}
        return token_count
    else:
        st_words=[porter_stemmer.stem                  (word)                   for (word) in nltk.word_tokenize(doc)                   if word not in stop_words and                   word not in string.punctuation]
        token_count={token:st_words.count(token) for token in set(st_words)}
        
        return token_count


def tfidf(docs, normalize_None_or_Stem="None"):
    if normalize_None_or_Stem=="None":
        docs_tokens={idx:get_doc_tokens(doc,"None")                  for idx,doc in enumerate(docs)}

        dtm=pd.DataFrame.from_dict(docs_tokens, orient="index" )
        dtm=dtm.fillna(0)
      
        tf=dtm.values
        doc_len=tf.sum(axis=1)
        tf=np.divide(tf.T, doc_len).T
    
        df=np.where(tf>0,1,0)
        
        smoothed_idf=np.log(np.divide(len(docs)+1, np.sum(df, axis=0)+1))+1    
        smoothed_tf_idf=tf*smoothed_idf
    
        return smoothed_tf_idf
    else:
        docs_tokens={idx:get_doc_tokens(doc,"Stem")                  for idx,doc in enumerate(docs)}

        dtm=pd.DataFrame.from_dict(docs_tokens, orient="index" )
        dtm=dtm.fillna(0)
      
        tf=dtm.values
        doc_len=tf.sum(axis=1)
        tf=np.divide(tf.T, doc_len).T
    
        df=np.where(tf>0,1,0)
        
        smoothed_idf=np.log(np.divide(len(docs)+1, np.sum(df, axis=0)+1))+1    
        smoothed_tf_idf=tf*smoothed_idf
    
        return smoothed_tf_idf
import csv
 
docs=[]
with open("amazon_review_300.csv","r") as f:
    reader=csv.reader(f)
    for line in reader:
        docs.append(line[2])

tfidf(docs,"None")
tfidf(docs,"Stem")


from scipy.spatial import distance

len(tfidf(docs,"None")[0])
smoothed_tf_idf = tfidf(docs,"None") 
("Size of TF-IDF matrix WithOut Stemming {}".format(len(smoothed_tf_idf[0])))


similarity=1-distance.squareform(distance.pdist(tfidf(docs,"None"), 'cosine'))
#similarity

# find top doc similar to first one
np.argsort(similarity)[:,::-1][0,0:5]

for idx, doc in enumerate(docs):
    print(idx,doc)


len(tfidf(docs,"Stem")[0])
smoothed_tf_idf = tfidf(docs,"Stem") 
("Size of TF-IDF matrix With Stemming {}".format(len(smoothed_tf_idf[0])))


similarity=1-distance.squareform(distance.pdist(tfidf(docs,"Stem"), 'cosine'))
#similarity

# find top doc similar to first one
np.argsort(similarity)[:,::-1][0,0:5]

for idx, doc in enumerate(docs):
    print(idx,doc)


# In[4]:


len(tfidf(docs,"None")[0])


# In[5]:


len(tfidf(docs,"Stem")[0])


# In[ ]:




