
# coding: utf-8

# In[32]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
import json
from numpy.random import shuffle
from nltk.cluster import KMeansClusterer, cosine_distance
from sklearn import metrics
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import precision_recall_fscore_support
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer


# In[33]:


data=json.load(open('ydata_3group.json','r'))
shuffle(data)
text,first_label,all_labels=zip(*data)
text=list(text)
first_label=list(first_label)
all_labels=list(all_labels)
tfidf_vect = TfidfVectorizer(stop_words="english", min_df=5)
dtm= tfidf_vect.fit_transform(text)
print("Size of the dtm Array\n")
print (dtm.shape)
num_clusters=3
clusterer = KMeansClusterer(num_clusters,                             cosine_distance, repeats=10)
clusters = clusterer.cluster(dtm.toarray(),                              assign_clusters=True)
#print(clusters[0:5])
df=pd.DataFrame(list(zip(first_label, clusters)),                 columns=['actual_class','cluster'])
print("First five cluster assignment\n")
df.head()
pd.crosstab( index=df.cluster, columns=df.actual_class)
cluster_dict={0:'T3', 1:"T1",              2:'T2'}
predicted_target=[cluster_dict[i] for i in clusters]
print("Classification report against Ground Truth\n")
print(metrics.classification_report      (first_label, predicted_target))
centroids=np.array(clusterer.means())
sorted_centroids = centroids.argsort()[:, ::-1] 
voc_lookup= tfidf_vect.get_feature_names()
for i in range(num_clusters):
    top_words=[voc_lookup[word_index]                for word_index in sorted_centroids[i, :20]]
    print("Cluster %d: %s " % (i, "; ".join(top_words)))


# In[23]:


data=json.load(open('ydata_3group.json','r'))
shuffle(data)
text,first_label,all_labels=zip(*data)
text=list(text)
first_label=list(first_label)
all_labels=list(all_labels)
tf_vectorizer = CountVectorizer(max_df=0.90,                 min_df=50, stop_words='english')
tf = tf_vectorizer.fit_transform(text)
tf_feature_names = tf_vectorizer.get_feature_names()
print("tf first 10 names\n")
print(tf_feature_names[0:10])
print("tf shape\n")
print(tf.shape)
num_topics = 3
lda = LatentDirichletAllocation(n_components=num_topics,                                 max_iter=10,verbose=1,
                                evaluate_every=1, n_jobs=1,
                                random_state=0).fit(tf)
num_top_words=20
print("Top 3 Topics and Top 20 words in each topic\n")
for topic_idx, topic in enumerate(lda.components_):
    print ("Topic %d:" % (topic_idx))
    # print out top 20 words per topic 
    words=[(tf_feature_names[i],topic[i]) for i in topic.argsort()[::-1][0:num_top_words]]
    print(words)
    print("\n")
topic_assign=lda.transform(tf)
print("Probability distribution of Topics for first 5 samples\n")
print(topic_assign[0:5])
topics=np.copy(topic_assign)
x1=np.argsort(topics)
y=x1[:,::-1]
y=[(row[1][0])           for row in enumerate(y)]
df=pd.DataFrame(list(zip(first_label, y)),                 columns=['actual_class','Topic'])
df.head()
pd.crosstab( index=df.Topic, columns=df.actual_class)
cluster_dict={0:'T3', 1:"T1",              2:'T2'}
predicted_target=[cluster_dict[i] for i in y]
print(metrics.classification_report      (first_label, predicted_target))


# In[24]:


cluster_dict={0:'T3', 1:"T1",              2:'T2'}
predicted_target=[cluster_dict[i] for i in y]
print(metrics.classification_report      (first_label, predicted_target))


# In[25]:


mlb = MultiLabelBinarizer()
Y=mlb.fit_transform(all_labels)
Y.shape
Y1=pd.DataFrame(Y,columns=['T1','T2','T3'])
Y1=Y1.reindex(columns=['T3','T1','T2'])


# In[26]:


p=[]
r=[]
f=[]
ptrs=[]
prob_threshold=0
while prob_threshold<1:
    topics1=np.where(topic_assign>=prob_threshold, 1, 0)
    precision, recall, fscore, support=    precision_recall_fscore_support(    Y1, topics1)
    p.append(precision)
    r.append(recall)
    f.append(fscore)
    ptrs.append(prob_threshold)
    prob_threshold+=.05


# In[27]:


dfdf = pd.DataFrame(p, columns=['PrecisionTopic1','PrecisionTopic2','PrecisionTopic3'])
dfdf1 = pd.DataFrame(r, columns=['RecallTopic1','RecallTopic2','RecallTopic3'])
dfdf2 = pd.DataFrame(f, columns=['FScoreTopic1','FScoreTopic2','FScoreTopic3'])


# In[28]:


dfdf["Threshold"]=ptrs
dfdf1["Threshold"]=ptrs
dfdf2["Threshold"]=ptrs
print("Table precision \n")
print(dfdf)
print("Table Recall \n")
print(dfdf1)
print("Table FScore \n")
print(dfdf2)


# In[29]:


print("Precision - Threshold Plot\n")
dfdf.groupby('Threshold')['PrecisionTopic1','PrecisionTopic2','PrecisionTopic3'].mean().plot(kind='line', figsize=(8,4)).legend(loc='center left', bbox_to_anchor=(1, 0.5));  # set legend


# In[30]:


print("Recall - Threshold Plot\n")
dfdf1.groupby('Threshold')['RecallTopic1','RecallTopic2','RecallTopic3'].mean().plot(kind='line', figsize=(8,4)).legend(loc='center left', bbox_to_anchor=(1, 0.5));  # set legend


# In[31]:


print("F-Score - Threshold Plot\n")
dfdf2.groupby('Threshold')['FScoreTopic1','FScoreTopic2','FScoreTopic3'].mean().plot(kind='line', figsize=(8,4)).legend(loc='center left', bbox_to_anchor=(1, 0.5));  # set legend

