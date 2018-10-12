
# coding: utf-8

# In[ ]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import re    
import nltk

def tokenize(text):
    text=text.lower()
    pattern=r'[^\-\_]\w[\w\-\_]+\w[^\-\_]'     
    tokens=nltk.regexp_tokenize(text, pattern)
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    filtered_tokens=[word                      for word in tokens                      if word not in stop_words]
    print(filtered_tokens)
    return(filtered_tokens)

text='''`strange days' chronicles the last two days of 1999 in los angeles. 
 as the locals gear up for the new millenium , lenny nero (ralph fiennes) goes about his business of peddling erotic 
 memory clips.  he pines for his ex-girlfriend, faith (juliette lewis), but doesn't notice that another friend, 
 mace (angela bassett) really cares for him.  this film features good performances, impressive film-making technique and 
 breath-taking crowd scenes.  director kathryn bigelow knows her stuff and does not hesitate to use it. 
 but as a whole, this is an unsatisfying movie. 
 the problem is that the writers, james cameron and jay cocks , were too ambitious, aiming for a film with social relevance, thrills, and drama. 
 not that ambitious film-making should be discouraged; just that when it fails to achieve its goals, it fails badly and 
 obviously.  the film just ends up preachy, unexciting and uninvolving.''' 
 


tokenize(text);


def sentiment_analysis(text, positive_words, negative_words):
    
    tokens = nltk.word_tokenize(text) 

    with open("positive-words.txt",'r') as f:
        positive_words=[line.strip() for line in f]


    positive_tokens=[token for token in tokens                  if token in positive_words]

    #print(positive_tokens)

    with open("negative-words.txt",'r') as f:
        negative_words=[line.strip() for line in f]


    negative_tokens=[token for token in tokens                  if token in negative_words]

    #print(negative_tokens)



    negations=['not', 'too', 'n\'t', 'no', 'cannot', 'neither','nor']
      




    for idx, token in enumerate(tokens):
        if token in positive_words:
            if idx>0:
                if tokens[idx-1] not in negations:
                    positive_tokens.append(token)
            else:
                positive_tokens.append(token)


    #print(positive_tokens)



    for idx, token in enumerate(tokens):
        if token in negative_words:
            if idx>0:
                if tokens[idx-1] not in negations:
                    negative_tokens.append(token)
            else:
                negative_tokens.append(token)


    #print(negative_tokens)

    pos={key:tokens.count(key) for key in positive_tokens}
    neg={key:tokens.count(key) for key in negative_tokens}
    pos
    neg
    pos_sum= sum(pos.values())
    #print("Positive Word Sum=",pos_sum)
    neg_sum=sum(neg.values())
    #print("Negative Word Sum=",neg_sum)

    Sentiment = 0
    if pos_sum>neg_sum:
        Sentiment = 2
    else:
        Sentiment = 1

    #print(Sentiment)
    return Sentiment

sentiment_analysis(text, positive_words, negative_words);

import csv

def performance_evaluate(input_file, positive_words, negative_words):
    
    Accuracy=None

    with open(input_file, "r") as f:
        # read a csv file delimited by \t" 
        reader=csv.reader(f, delimiter=',') 
        # each row is a list of strings
        # use int/float to convert strings to numbers
        rows=[(row[1][0],row[1][2])               for row in enumerate(reader)  if row[1][0] =='2']       
    int(rows[1][0])
    len(rows)
    #rows
    rows
    # write your code here
    x=0
    i=0
    z=0

    for i in range(len(rows)):
        sen_result = sentiment_analysis(rows[i][1], positive_words, negative_words);
        if sen_result == 2:
            z+=1
        else:
            z+=0
        #x+=1
        #i+=1
    
    print(z)
    Accuracy =z/len(y)
    print(Accuracy)
    return Accuracy

performance_evaluate("amazon_review_300.csv", positive_words, negative_words);

