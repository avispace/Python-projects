#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import numpy as np


#1) Read from a csv file named Customer.csv, convert it into a pandas dataframe, and displays the entire data.
cus_data = pd.read_csv('Customer.csv', sep=',', header=0)
cus_data
#checking the shape of the df
cus_data.shape


#2) (1point) Display the 333th customer’s information
cus_data.loc[332]


#3) (1point) Display all male customers
cus_data[cus_data['Gender']=='male']


#4) (1point) Display age and payment method data for the last 15 customers
cus_data.loc[(1000-15):, ['Age', 'Payment Method']]


#5) (1point) Display age and payment method data for the youngest 10customers
cus_sorted = cus_data.sort_values(by='Age', ascending=True, ignore_index=True)
cus_sorted.loc[0:10, ['Age', 'Payment Method']]


#6) (1point) Permanently remove customers who are either too old (older than 120 years)
            #or too young (younger than 14 years) from the dataset
cus_data = cus_data[(cus_data['Age']<= 120) & (cus_data['Age']>14)]
#verifying if the effect was permament
cus_data.sort_values(by='Age', ascending=True, ignore_index=True)


# In[4]:





# In[5]:





# In[8]:





# In[13]:





# In[15]:





# In[16]:





# In[ ]:




