#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


df = pd.read_csv('web-page-phishing.csv')



# In[5]:


df.head()


# In[7]:


cat_col = ['n_at','n_tilde','n_redirection']
for i in cat_col:
    print(i)
    df[i] = df[i].fillna(df[i].median())


# In[31]:


sns.histplot(df['phishing'],legend=True,color='Red',stat='percent')
plt.title('Distribution of Phishing Labels (0 = Legit, 1 = Phishing)')


# In[63]:


X = df.loc[:, ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
               'n_questionmark', 'n_redirection']]
Y = df['phishing']


# In[71]:


import seaborn as sns
import matplotlib.pyplot as plt

def plot_top10_histograms(data, color='skyblue'):
  
   
    for column in data.columns:
        # Get top 10 frequent values and their counts
        top10 = data[column].value_counts().nlargest(10).sort_index()
        
        plt.figure(figsize=(6, 4))
        sns.barplot(x=top10.index, y=top10.values, color=color)
        plt.title(f'Top 10 Frequency Values of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

# Example usage
X = df.loc[:, ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
               'n_questionmark', 'n_redirection']]

plot_top10_histograms(X, color='purple')


# In[75]:


import seaborn as sns
import matplotlib.pyplot as plt

def plot_top10_for_phishing_only(X, Y, color='red'):

    
    phishing_data = X[Y == 1]  # Filter only phishing = 1

    for column in phishing_data.columns:
        top10 = phishing_data[column].value_counts().nlargest(10).sort_index()

        plt.figure(figsize=(6, 4))
        sns.barplot(x=top10.index, y=top10.values, color=color)
        plt.title(f'Top 10 {column} values (phishing = 1)')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

# Example usage
X = df.loc[:, ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
               'n_questionmark', 'n_redirection']]
Y = df['phishing']

plot_top10_for_phishing_only(X, Y)


# In[ ]:




