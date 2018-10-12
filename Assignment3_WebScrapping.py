
# coding: utf-8

# In[ ]:


import requests                   

# import BeautifulSoup from package bs4 (i.e. beautifulsoup4)
from bs4 import BeautifulSoup 

def getReviews(movie_id):
    page_url = requests.get("https://www.rottentomatoes.com/m/"+movie_id+"/reviews/?type=top_critics")    # send a get request to the web page
    reviews=[]

# status_code 200 indicates success. 
#a status code >200 indicates a failure 
    if page_url.status_code==200:        
        soup = BeautifulSoup(page_url.content, 'html.parser')
    
    
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

