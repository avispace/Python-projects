#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, re
response=requests.get("https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3&page=1&locId=1154532&locType=C&locName=Boston,%20MA%20(US)&filterType=RATING_OVERALL")
html_source=str(response.text)
print(html_source)


# In[3]:


#import required files
import requests, re, sqlite3

regER = "<h2 data-test=\"employer-short-name\">(.*?)<\/h2><div class=\".*?\"><span class=\".*?\" data-test=\"rating\"><b>(.*?)<\/b><\/span>"
regRev = "<h3 class=\".*?\" data-test=\"cell-Reviews-count\">(.*?)<\/h3><div><span class=\".*?\">Reviews<\/span><\/div><\/div>"
regSal = "<h3 class=\".*?\" data-test=\"cell-Salaries-count\">(.*?)<\/h3><div><span class=\".*?\">Salaries<\/span><\/div><\/div>"
regJob = "<h3 class=\".*?\" data-test=\"cell-Jobs-count\">(.*?)<\/h3><div><span class=\".*?\">Jobs<\/span><\/div><\/div>"
regSize = "<span class=\".*?\" data-test=\"employer-size\">(.*?)<\/span>"
regInd = "<span class=\".*?\" data-test=\"employer-industry\">(.*?)<\/span>"



matchER=re.compile(regER,re.S|re.I).findall(html_source)
matchRev=re.compile(regRev,re.S|re.I).findall(html_source)
matchSal=re.compile(regSal,re.S|re.I).findall(html_source)
matchJob=re.compile(regJob,re.S|re.I).findall(html_source)
matchSize=re.compile(regSize,re.S|re.I).findall(html_source)
matchInd=re.compile(regInd,re.S|re.I).findall(html_source)


#prepare the database for stroing results
conn = sqlite3.connect('g1.db')
c = conn.cursor()
c.execute("CREATE TABLE gd(              EmployerName varchar(50),               Rating varchar(50))")

#extract each element and feed it into sql
for m in matchER:
    EmployerName = m[0]
    Rating = m[1]
    #Insert into sql database
    query = "INSERT INTO gd VALUES (?, ?)"
    c.execute(query, (EmployerName,Rating))
    conn.commit()
    
c.execute("SELECT * FROM gd")
result = c.fetchall()

print(result)

c.close()
conn.close()  


# In[ ]:




