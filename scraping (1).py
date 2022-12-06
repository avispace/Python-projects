#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests, re
import time
import sqlite3
from selenium import webdriver

#Step 1: Get the webpage into SQL database (using webdrive)
driver = webdriver.Chrome() # you need to download Chrome webdriver and save it in PATH variable.
URL_pattern_str="https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page=$NUM$"

page_URL=URL_pattern_str.replace("$NUM$",str(1))
print("Starting with:"+page_URL)
driver.get(page_URL)
page_content = driver.page_source

#prepare the database for stroing results
conn = sqlite3.connect('gd.db')
c = conn.cursor()
c.execute("CREATE TABLE glassd (            EmployerName varchar(100),            Rating varchar(100),            Reviews varchar(100),            Salaries varchar(100),            Jobs varchar(100),            Size varchar(100),            Industry varchar(100))")

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
                if (len(matches) > 1):
                    pass #move on to next one
                else: # len(matche) == 1
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
                    
                    #parsing Description
                    matches=re.compile(r'<b>Description</b></span><div><p class="css-1sj9xzx css-56kyx5">(.*?)</p></div></div></div></div>', re.S|re.I).findall(chunk) 
                    if(len(matches)>0):
                        Description=matches[0] 
            
                    # printing collected data to screen
                    #print(EmployerName +":"+ Rating +":"+ Reviews +":"+ Salaries +":"+ Jobs +":"+ Size+":"+ Industry+":"+ Description) 
                    #Save the extracted data into the database
                    query = "INSERT INTO glassd VALUES (?, ?, ?, ?, ?, ?,?,?)"
                    c.execute(query, (EmployerName, Rating, Reviews, Salaries, Jobs, Size, Industry,Description))
            
                    if i > 12:break;
                    else:
                        #get next review page
                        page_URL=URL_pattern_str.replace("$NUM$",str(i+1))
                        print("Collecting reviews from: "+page_URL)
                        time.sleep(1) # a good practice is to wait a little time between each HTTP request
                        driver.get(page_URL)
                        page_content=driver.page_source   # getting HTML source of page i


conn.commit()
c.execute("SELECT * FROM glassd")
result = c.fetchall()
print(result)

conn.close()

driver.close()
print("\n\nCollection Finished!")           
            


# In[3]:


# Step 2: Visualize the SQL database

# create connection and cursor
conn = sqlite3.connect ('gd.db')
cursor = conn. cursor()
                        
# execute SQL query. In this example, show all data in [pokemon meta] table
cursor.execute ("SELECT * from [glassd]")
rows=cursor.fetchall()
                        
# print the column names of the table
header= ""
for column_info in cursor.description:
    header+=column_info[0]+","
print(header)
                        
#print the table content
for row in rows:
    print (row)
                        
#close connection after using it
conn.close()


# In[4]:


#Step 3: Store SQL data into dataframe for further analysis
import sqlite3
import os
import pandas as pd

conn = sqlite3.connect('gd.db') 
c = conn.cursor()
                 
c.execute ("SELECT * from [glassd]")

gddf = pd.DataFrame(c.fetchall(), columns = ['EmployerName', 'Rating', 'Reviews', 'Salaries', 'Jobs', 'Size', 'Industry'])
print (gddf)

#gddf.to_csv("glassdoor.csv") 


# In[ ]:


# Step 4: Analytics

#Initial data exploration



#a) Descriptive analysis:

#b) Visualization

#c) Regression

#d) Sentiment analysis
#e) Other text mining analysis

