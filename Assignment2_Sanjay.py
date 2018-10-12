
# coding: utf-8

# In[7]:


#Solution Assignment 2 Sanjay K Pattanayak
#Import statements
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import numpy as np
import pandas as pd
import csv
import os, sys

#Solution Question 1
def analyze_tf(arr):

    tf_i=None
    #copying the array to a variable x, takes the array as an input
    x=np.copy(arr)
    print(x)
    #getting the sum of rows to get the document size(length of the document)
    y=np.sum(x, axis=1, keepdims=True)
    print(y)
    #normalizes the frequency of each 
    #word as: word frequency divided by the length of the document. 
    #Save the result as an array named tf (i.e. term frequency)
    tf = x/y
    print(tf)
    # Fill the term-frequency matrix 
    # with binary values (1: present, 0: not present)
    z=np.where(x>0,1,0)
    print(z)
    # count document frequency of each word 
    # the number of documents that contain the word
    #calculates the document frequency (df) of each word, e.g. how many documents contain a specific word
    df=np.sum(z, axis=0)
    print(df)
    #calculates tf_idf array as: tf / df (tf divided by df)
    tf_i=tf/df
    print(tf_i)
    #for each document, finds the indexes of words with top 3 largest values in the tf_idf array. Prints out these indexes.
    a=np.argsort(tf_i)
    print(a)
    print(a[:,::-1][:,0:3])
    #returns the tf_idf array.   
    return tf_i
#Test Q1
arr=np.random.randint(0,3,(4,8))

tf_idf=analyze_tf(arr)

# Solution Question 2
def analyze_cars():
    
    #Read "cars.csv" as a dataframe with the first row in the csv file as column names
    p2=pd.read_csv('cars.csv', header=0)
    print(p2)
    #Sort the data by "cylinders" and "mpg" in decending order and report the first three rows after sorting
    print(p2.columns)
    print(p2.sort_values(by=["cylinders","mpg"],ascending=False).head(3))
    p1=p2.sort_values(by=["cylinders","mpg"],ascending=False)
    print(p1)
    print(p1.head(3))
    #Create a new column called "brand" to store the brand name 
    #as the first word in "car" column (using "apply" function)
    p1['brand']=p1.apply(lambda row:         (row["car"].split(" "))[0], axis=1)
    print(p1)
    #Show the mean, min, and max acceleration values by "cylinders" for each of these brands: "ford", "buick" and "honda"
    #Filtering the table
    p4=p1[(p1.brand.isin(['ford','buick','honda']))]
    print(p4)
    #Grouping the table
    grouped= p4.groupby(['brand','cylinders'])
    #Taking aggregate functions
    print(grouped['acceleration'].agg([np.min, np.mean, np.max]))
    #Creates a cross tab to show the average mpg of each brand and each cylinder value. 
    #Uses "brand" as row index and "clinders" as column index.
    print(pd.crosstab(index=p1.brand, columns=p1.cylinders, values=p1.mpg, aggfunc=np.mean ))
    return()

analyze_cars()

