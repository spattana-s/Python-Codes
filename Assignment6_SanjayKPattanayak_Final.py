
# coding: utf-8

# In[70]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import svm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


print("Solution for Question 1:\n")
with open("amazon_review_300.csv", "r") as f:
    reader=csv.reader(f, delimiter=',') 
    rows=[(row[1][2],row[1][0])           for row in enumerate(reader)]

text,target=zip(*rows)
text=list(text)
target=list(target)
tfidf_vect = TfidfVectorizer(stop_words="english") 
dtm= tfidf_vect.fit_transform(text)
metrics = ['precision_macro', 'recall_macro', "f1_macro"]
clf = MultinomialNB()
cv = cross_validate(clf, dtm, target, scoring=metrics, cv=6)
print("Test data set average precision:")
print(cv['test_precision_macro'])
print("\nTest data set average recall:")
print(cv['test_recall_macro'])
print("\nTest data set average fscore:")
print(cv['test_f1_macro'])
print("\nTrain data set average fscore:")
print(cv['train_f1_macro'])


# In[ ]:


print("Solution for Question 2:\n")
text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', MultinomialNB())
                   ])

parameters = {'tfidf__min_df':[1,2,3,5],
              'tfidf__stop_words':[None,"english"],
              'clf__alpha': [0.5,1.0,1.5,2.0],
}

metric =  "f1_macro"
gs_clf = GridSearchCV(text_clf, param_grid=parameters, scoring=metric, cv=6)
gs_clf = gs_clf.fit(text, target)
for param_name in gs_clf.best_params_:
    print(param_name,": ",gs_clf.best_params_[param_name])

print("best f1 score:", gs_clf.best_score_)


# In[ ]:


print("Solution for Question 3:\n")
with open("amazon_review_large.csv", "r") as f:
    reader=csv.reader(f, delimiter=',') 
    rows=[(row[1][1],row[1][0])           for row in enumerate(reader)]       
df=[]
i=400
while i<=20000:
    text,target=zip(*rows[0:i])
    text=list(text)
    target=list(target)
    tfidf_vect = TfidfVectorizer(stop_words="english") 
    dtm= tfidf_vect.fit_transform(text)
    metrics = ['precision_macro', 'recall_macro', "f1_macro"]
    clf = svm.LinearSVC()
    cv = cross_validate(clf, dtm, target, scoring=metrics, cv=5)
    x=(np.mean(np.array(cv['test_f1_macro'])))
    y=(i,x)
    df.append(y)
    i+=400
#df
df1=[]
i=400
while i<=20000:
    text,target=zip(*rows[0:i])
    text=list(text)
    target=list(target)
    tfidf_vect = TfidfVectorizer(stop_words="english") 
    dtm= tfidf_vect.fit_transform(text)
    metrics = ['precision_macro', 'recall_macro', "f1_macro"]
    clf = MultinomialNB()
    cv = cross_validate(clf, dtm, target, scoring=metrics, cv=10)
    x=(np.mean(np.array(cv['test_f1_macro'])))
    y=(i,x)
    df1.append(y)
    i+=400
#df1
dfdf = pd.DataFrame(df, columns=['SampleSize','AvgF1'])
print("SVM Classifier")
print(dfdf)


dfdf1 = pd.DataFrame(df1, columns=['SampleSize','AvgF1'])
print("Naive Bayes Classifier\n")
print(dfdf1)


# In[ ]:


print("SVM Classifier Plot\n")
plt.plot(dfdf.SampleSize,dfdf.AvgF1);


# In[ ]:


print("Naive-Bayes Classifier Plot\n")
plt.plot(dfdf1.SampleSize,dfdf1.AvgF1);

