#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import required files
import requests, re, sqlite3

#get website
response=requests.get("https://www.cbinsights.com/research-unicorn-companies")
html_source=str(response.text)

#regex code and matches to regex
regex = "<td>.*?\">(.*?)<\/a><\/td>\W*?<td data-value=\".*?\">(.*?)<\/td>\W*?<td>(.*?)<\/td>\W*?<td>(.*?)<\/td>\W*?<td>(.*?)<\/td>\W*?<td>(.*?)<\/td>\W*?<td>(.*?)<\/td>"
matches=re.compile(regex,re.S|re.I).findall(html_source)

  
#prepare the database for storing results
conn = sqlite3.connect('Unicorns.db')
c = conn.cursor()
c.execute("CREATE TABLE Unicorns(              Company varchar(100),               Valuation varchar(20),               DateJoined varchar(50),               Country varchar(50),               City varchar(50),               Industry varchar(50),               Investor varchar(300))")

#extract each element and feed it into sql
for m in matches:
    companyname = m[0] 
    valuation = m[1]
    datejoined = m[2]
    country = m[3]
    city = m[4]
    industry = m[5]
    investors = m[6]
    #Insert into sql database
    query = "INSERT INTO Unicorns VALUES (?, ?, ?, ?, ?, ?, ?)"
    c.execute(query, (companyname,valuation,datejoined,country,city,industry,investors))
    conn.commit()
    
c.execute("SELECT * FROM Unicorns")
result = c.fetchall()

print(result)

c.close()
conn.close()  

