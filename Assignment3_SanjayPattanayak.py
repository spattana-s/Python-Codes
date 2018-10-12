
# coding: utf-8

# In[ ]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# plot charts inline
get_ipython().magic('matplotlib inline')


df = pd.read_csv('auto-mpg.csv', header=0)
df.head()
df.info()

df=df.dropna(axis=0, how='any')  
df.info()

# Exercise 4.2.1. line chart

# How does mpg/weight change over time?

# show the relationship between 
# average mpg/weight and model year
ctab=pd.crosstab(index=df.model_year, columns=df.origin, values=df.mpg, aggfunc=np.mean )
ctab

ctab.plot(kind='line', figsize=(8,4)).legend(loc='center left', bbox_to_anchor=(1, 0.5));  # set legend

# what finding can be seen here?

#Plot a line chart (with multiple lines) 
#to show the mpg trend over the years by origin. Your plot will be similar to the ﬁgure below


import requests                   

# import BeautifulSoup from package bs4 (i.e. beautifulsoup4)
from bs4 import BeautifulSoup 

def getReviews(movie_id):
    page_url = requests.get("https://www.rottentomatoes.com/m/"+movie_id+"/reviews/?type=top_critics")    # send a get request to the web page
    reviews=[]

# status_code 200 indicates success. 
#a status code >200 indicates a failure 
    if page_url.status_code==200:        
        soup = BeautifulSoup(page.content, 'html.parser')
    
    
        divs=soup.select("div.review_table_row")
    
    
        for idx, div in enumerate(divs):
        # for testing you can print idx, div
        #print idx, div 
        
        # initiate the variable for each period
            reviewer_name=None
            review_date=None
            review=None
            review_score=None
        
        # get title
            reviewer=div.select("div.critic_name")
            reviewer_name = reviewer[0].get_text()
        
            reviewdate=div.select("div.review_date")
            review_date = reviewdate[0].get_text()
        
            reviewcomment=div.select("div.the_review")
            review = reviewcomment[0].get_text()
        
            reviewscore=div.select("div.review_desc div.small.subtle")
            review_score = reviewscore[0].get_text()
         
            
        # add title, description, and temperature as a tuple into the list
            reviews.append((reviewer_name, review_date, review, review_score))
            
        return(reviews)

    
getReviews("star_wars_the_last_jedi")

