#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests, re
import time
import sqlite3
from selenium import webdriver

#Step 1: Get the webpage (using webdrive)
driver = webdriver.Chrome() # you need to download Chrome webdriver and save it in PATH variable.
URL_pattern_str="https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3&page=$NUM$&locId=1154532&locType=C&locName=Boston,%20MA%20(US)&filterType=RATING_OVERALL"

page_URL=URL_pattern_str.replace("$NUM$",str(1))
print("Starting with:"+page_URL)
driver.get(page_URL)
page_content = driver.page_source

#Collecting reviews from all pages
for i in range(1, 11):
    all_chunks=re.compile(r"employer-card-single(.*?)</p>",re.S|re.I).findall(page_content)  
    if len(all_chunks)>0:  # if found any
        for chunk in all_chunks:

            #print(chunk)
            
            #initialization
            EmployerName=""
            Rating=""
            Reviews="" 
            Salaries=""
            Jobs = ""
            Size = ""
            Industry = ""
            
            #parsing EmployerName
            matches=re.compile(r"employer-short-name\">(.*?)</h2>",re.S|re.I).findall(chunk)  
            if(len(matches)>0):
                EmployerName=matches[0]
                
            #parsing Rating
            matches=re.compile(r"data-test=\"rating\"><b>(.*?)<\/b>" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                Rating=matches[0].strip()
                
            #parsing Reviews
            matches=re.compile(r"cell-Reviews-count\">(.*?)<\/h3><div><span class=\".*?\">Reviews<" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                Reviews=matches[0]
                
            #parsing Salaries
            matches=re.compile(r"cell-Salaries-count\">(.*?)<\/h3><div><span class=\".*?\">Salaries<" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                Salaries=matches[0]
                
            #parsing Jobs
            matches=re.compile(r"cell-Jobs-count\">(.*?)<\/h3><div><span class=\".*?\">Jobs<" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                Jobs=matches[0]
                
            #parsing Size
            matches=re.compile(r"employer-size\">(.*?)<\/span>" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                Size=matches[0]
                
            #parsing Industry
            matches=re.compile(r"employer-industry\">(.*?)<\/span>" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                Industry=matches[0]
            
            if i > 12:break;
            else:
                #get next review page
                page_URL=URL_pattern_str.replace("$NUM$",str(i+1))
                print("Collecting reviews from: "+page_URL)
                time.sleep(1) # a good practice is to wait a little time between each HTTP request
                driver.get(page_URL)
                page_content=driver.page_source   # getting HTML source of page i

driver.close()
print("\n\nCollection Finished!")             
            


# In[ ]:


#Collecting reviews from all pages
for i in range(1, num_of_pages+1):
    all_chunks=re.compile(r"customer_review(.*?)ReportAbuse",re.S|re.I).findall(page_content)  
    if len(all_chunks)>0:  # if found any
        for chunk in all_chunks:

            #print(chunk)
            
            #initialization
            username=""
            country=""
            review_text="" 
            review_date=""
            num_helpful = ""
            num_star = ""
            
            #parsing username
            matches=re.compile(r"profile-name\">(.*?)<",re.S|re.I).findall(chunk)  
            if(len(matches)>0):
                username=matches[0]
                
            #parsing review text
            matches=re.compile(r"review-text-content.*?<span>(.*?)<\/span>" ,re.S|re.I).findall(chunk) 
            if(len(matches)>0):
                review_text=matches[0].strip()
                
## <span data-hook="review-body" class="a-size-base review-text review-text-content">
## <span>I like it but I can not adjust the color.but I like the Bluetooth.</span>
## </span>
                
            #parsing review stars ?????*****
            matches =re.compile(r'title="(.*?) out of 5 stars', re.S|re.I).findall(chunk)  
            if(len(matches)>0):
                num_star=matches[0].strip()

## <i data-hook="review-star-rating" class="a-icon a-icon-star a-star-4 review-rating"><span class="a-icon-alt">4.0 out of 5 stars</span></i>
                
            #parsing review date and country
            matches =re.compile(r'Reviewed in (\D*?) on (.*?)<\/span>', re.S|re.I).findall(chunk)  
            if(len(matches) == 1):
                country=matches[0][0].strip()
                review_date = matches[0][1].strip()
                
                
## <span data-hook="review-date" class="a-size-base a-color-secondary review-date">Reviewed in the United States on February 24, 2022</span>
            
            #parsing number of people found helpful
            matches =re.compile(r'(\d*? )people found this helpful', re.S|re.I).findall(chunk)  
            if(len(matches)>0):
                num_helpful=matches[0].strip()
             
            # printing collected data to screen
            #print(username +":"+ review_text +":"+ num_star +":"+ country +":"+ review_date +":"+ num_helpful) 
            #Save the extracted data into the database
            query = "INSERT INTO Reviews VALUES (?, ?, ?, ?, ?, ?)"
            c.execute(query, (username, review_text, country, review_date, num_star, num_helpful))
            
    #Is there a next page?
    matches = re.compile(r'<li class="a-disabled a-last">Next page<', re.S|re.I).findall(page_content)
    if len(matches) > 0:
        break;
    else:
        #get next review page
        page_URL=URL_pattern_str.replace("$NUM$",str(i+1))
        print("Collecting reviews from: "+page_URL)
        time.sleep(1) # a good practice is to wait a little time between each HTTP request
        driver.get(page_URL)
        page_content=driver.page_source   # getting HTML source of page i

conn.commit()
conn.close()

driver.close()
print("\n\nCollection Finished!")  

