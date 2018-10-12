
# coding: utf-8

# # <center>Assignment 1</center>

# ## 1. Define a function to analyze the frequency of words in a string ##
#  - Define a function named "**count_token**" which
#      * has a string as an input 
#      * splits the string into a list of tokens by space. For example, "hello world" will be split into two tokens ['hello','world']
#      * for the tokens, do the following in sequence:
#         * strips all leading and trailing space of each token
#         * removes a token if it contain no more than 1 character (use function *len* on each token, i.e. *len*(token)<=1)
#         * converts all tokens into lower case
#      * create a dictionary containing the count of every remaining token, e.g. {'is': 5, 'hello':1,...}
#      * returns the dictionary as the output
#      
# ## 2. Define a class to analyze a collection of documents ##
#  - Define a new class called "**Text_Analyzer**" which has the following:
#     - two variables: **input_file**, **output_file**. Initialize them using the class constructor.
#     - a function named "**analyze**" that:
#       * reads all lines from input_file and concatenate them into a string
#       * calls the function "count_token" to get a token-count dictionary 
#       * saves the dictionary into output_file with each key-value pair as a line delimited by comma (see "foo.csv" in Exercise 10.3 for examples).
#       
# ## 3. Define a function to analyze a numpy array
#  - Assume we have a array which contains term frequency of each document. Where each row is a document, each column is a word, and the value denotes the frequency of the word in the document. Define a function named "analyze_tf" which:
#       * takes the array as an input
#       * normalizes the frequency of each word as: word frequency divided by the length of the document. Save the result as an array named **tf** (i.e. term frequency)
#       * calculates the document frequency (**df**) of each word, e.g. how many documents contain a specific word
#       * calculates **tf_idf** array as: **tf / df** (tf divided by df). The reason is, if a word appears in most documents, it does not have the discriminative power and often is called a "stop" word. The inverse of df can downgrade the weight of such words.
#       * for each document, find out the **indexes of words with top 3 largest values in the tf_idf array**. Print out these indexes.
#       * return the tf_idf array.
#  - Note, for all the steps, ** do not use any loop**. Just use array functions and broadcasting for high performance computation.
#      
# 
# ## Submission Guideline##
# - Following the solution template provided below. Use __main__ block to test your functions and class
# - Save your code into a python file (e.g. assign1.py) that can be run in a python 3 environment. In Jupyter Notebook, you can export notebook as .py file in menu "File->Download as".
# - Make sure you have all import statements. To test your code, open a command window in your current python working folder, type "python assign1.py" to see if it can run successfully.

# In[35]:


# Structure of your solution to Assignment 1 

import numpy as np
import csv
import os, sys
os.chdir("C:/Users/sanja/Google Drive/2ndSem/BIA660C_WebAnalytics_RongLiu/Lectures/2.IntroToPython")
def count_token(text):
    
    #text =  ('Hi , This is the very first program of a Python function')
    
    
#    print (text.split(" "))
    list1 = (text.split(" "))
#    print (list1)
    list2 =[]
    list2 = [(x.strip() )   for x in list1             if len(x)>1]
#    print (list2)
    list3 =[]
    list3 = [x.lower() for x in list2]
#    print (list3)

    count_dict={}  # empty dictionary
    for x in list3:
        if x in count_dict:
            count_dict[x]+=1
        else:
            count_dict[x]=1
#    print(count_dict)
    
    
    return count_dict

text='''Hello world! This is a hello world example !'''   
print(count_token(text))

class Text_Analyzer(object):
    
    def __init__(self, input_file, output_file):
        self.inputF=input_file
        self.outputF=output_file
        # add your code
          
    def analyze(self):
        fin = open(self.inputF, "r")
        lines = fin.readlines()
        fin.close()
        dict_file={}
        dict_file = count_token(''.join(lines))
        print(dict_file)
        # use "with" statement to automatically 
        # close t_filethe file after completing the block   
        # write csv file
       
        with open(self.outputF, "w") as f:  
        # write to a csv file delimited 
        # by "\t" (you can set "," or other delimiters)                    
            writer=csv.writer(f, delimiter=',')          
            writer.writerows(dict_file.items())

analyzer=Text_Analyzer("foo.txt", "foo.csv")
vocabulary=analyzer.analyze()

