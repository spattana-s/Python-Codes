
# coding: utf-8

# In[37]:


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


# In[38]:


data=json.load(open('ydata_3group.json','r'))
shuffle(data)
text,first_label,all_labels=zip(*data)
text=list(text)
first_label=list(first_label)
all_labels=list(all_labels)
tfidf_vect = TfidfVectorizer(stop_words="english", min_df=5)
dtm= tfidf_vect.fit_transform(text)
print (dtm.shape)
num_clusters=3
clusterer = KMeansClusterer(num_clusters,                             cosine_distance, repeats=10)
clusters = clusterer.cluster(dtm.toarray(),                              assign_clusters=True)
print(clusters[0:5])
df=pd.DataFrame(list(zip(first_label, clusters)),                 columns=['actual_class','cluster'])
df.head()
pd.crosstab( index=df.cluster, columns=df.actual_class)
cluster_dict={0:'T3', 1:"T1",              2:'T2'}
predicted_target=[cluster_dict[i] for i in clusters]
print(metrics.classification_report      (first_label, predicted_target))
centroids=np.array(clusterer.means())
sorted_centroids = centroids.argsort()[:, ::-1] 
voc_lookup= tfidf_vect.get_feature_names()
for i in range(num_clusters):
    top_words=[voc_lookup[word_index]                for word_index in sorted_centroids[i, :20]]
    print("Cluster %d: %s " % (i, "; ".join(top_words)))


# In[3]:


data=json.load(open('ydata_3group.json','r'))
shuffle(data)
text,first_label,all_labels=zip(*data)
text=list(text)
first_label=list(first_label)
all_labels=list(all_labels)
tf_vectorizer = CountVectorizer(max_df=0.90,                 min_df=50, stop_words='english')
tf = tf_vectorizer.fit_transform(text)
tf_feature_names = tf_vectorizer.get_feature_names()
print(tf_feature_names[0:10])
print(tf.shape)
num_topics = 3
lda = LatentDirichletAllocation(n_components=num_topics,                                 max_iter=10,verbose=1,
                                evaluate_every=1, n_jobs=1,
                                random_state=0).fit(tf)
num_top_words=20
for topic_idx, topic in enumerate(lda.components_):
    print ("Topic %d:" % (topic_idx))
    # print out top 20 words per topic 
    words=[(tf_feature_names[i],topic[i]) for i in topic.argsort()[::-1][0:num_top_words]]
    print(words)
    print("\n")
topic_assign=lda.transform(tf)
print(topic_assign[0:5])
topics=np.copy(topic_assign)
x1=np.argsort(topics)
y=x1[:,::-1]
y=[(row[1][0])           for row in enumerate(y)]
df=pd.DataFrame(list(zip(first_label, y)),                 columns=['actual_class','Topic'])
df.head()
pd.crosstab( index=df.Topic, columns=df.actual_class)
cluster_dict={0:'T1', 1:"T2",              2:'T3'}
predicted_target=[cluster_dict[i] for i in y]
print(metrics.classification_report      (first_label, predicted_target))


# In[4]:


cluster_dict={0:'T1', 1:"T2",              2:'T3'}
predicted_target=[cluster_dict[i] for i in y]
print(metrics.classification_report      (first_label, predicted_target))


# In[6]:


rows=[(row[1][0])           for row in enumerate(all_labels)]
#rows
prob_threshold=0.05
topics=np.copy(topic_assign)
while prob_threshold<=1:
    topics1=np.where(topics>=prob_threshold, 1, 0)
    #print(topics[0:5])
    #print(topics1[0:5])
    x=topics*topics1
    #x
    x1=np.argsort(x)
    y=x1[:,::-1]
    y=[(row[1][0])           for row in enumerate(y)]
    df=pd.DataFrame(list(zip(rows, y)),                 columns=['actual_class','Topic'])
    df.head()
    pd.crosstab( index=df.Topic, columns=df.actual_class)
    cluster_dict={0:'T1', 1:"T2",              2:'T3'}
    predicted_target=[cluster_dict[i] for i in y]
    print(metrics.classification_report      (rows, predicted_target))
    prob_threshold+=.05


# In[ ]:


rows=[(row[1][0])           for row in enumerate(all_labels)]
#rows
p=[]
r=[]
f=[]
ptrs=[]
prob_threshold=0.05
topics=np.copy(topic_assign)
while prob_threshold<=1:
    topics1=np.where(topics>=prob_threshold, 1, 0)
    #print(topics[0:5])
    #print(topics1[0:5])
    x=topics*topics1
    #x
    x1=np.argsort(x)
    y=x1[:,::-1]
    y=[(row[1][0])           for row in enumerate(y)]
    df=pd.DataFrame(list(zip(rows, y)),                 columns=['actual_class','Topic'])
    df.head()
    pd.crosstab( index=df.Topic, columns=df.actual_class)
    cluster_dict={0:'T1', 1:"T2",              2:'T3'}
    predicted_target=[cluster_dict[i] for i in y]
    print(metrics.classification_report      (rows, predicted_target))
    precision, recall, fscore, support=    precision_recall_fscore_support(    rows, predicted_target)
    a=(precision,prob_threshold)
    b=(recall,prob_threshold)
    c=(fscore,prob_threshold)
    #p.append(a)
    #r.append(b)
    #f.append(c)
    p.append(precision)
    r.append(recall)
    f.append(fscore)
    ptrs.append(prob_threshold)
    prob_threshold+=.05


# In[19]:


x=np.mean(p,axis=1)
y=np.mean(r,axis=1)
z=np.mean(f,axis=1)


# In[27]:


dfdf = pd.DataFrame(x, columns=['Precision'])
dfdf1 = pd.DataFrame(y, columns=['Recall'])
dfdf2 = pd.DataFrame(z, columns=['FScore'])


# In[48]:


dfdf["Threshold"]=ptrs
dfdf1["Threshold"]=ptrs
dfdf2["Threshold"]=ptrs
print("Table precision \n")
print(dfdf)
print("Table Recall \n")
print(dfdf1)
print("Table FScore \n")
print(dfdf2)


# In[49]:


print("Precision - Threshold Plot\n")
plt.plot(dfdf.Precision,dfdf.Threshold);
plt.xlabel('Precision', fontsize=16)
plt.ylabel('Threshold', fontsize=16)


# In[50]:


print("Recall - Threshold Plot\n")
plt.plot(dfdf1.Recall,dfdf1.Threshold);
plt.xlabel('Recall', fontsize=16)
plt.ylabel('Threshold', fontsize=16)


# In[51]:


print("FScore - Threshold Plot\n")
plt.plot(dfdf2.FScore,dfdf2.Threshold);
plt.xlabel('FScore', fontsize=16)
plt.ylabel('Threshold', fontsize=16)

