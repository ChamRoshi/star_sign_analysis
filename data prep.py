#!/usr/bin/env python
# coding: utf-8

# In[2]:

import pandas as pd
import spacy
nlp = spacy.load("en_core_web_md")
import numpy as np

# In[3]:


df = pd.read_excel("dated_births.xlsx")
df = df[df.birthday != ""]
df.head()


# In[4]:


zodiacs = [(120, 'Cap'), (218, 'Aqu'), (320, 'Pis'), (420, 'Ari'), (521, 'Tau'),
           (621, 'Gem'), (722, 'Can'), (823, 'Leo'), (923, 'Vir'), (1023, 'Lib'),
           (1122, 'Sco'), (1222, 'Sag'), (1231, 'Cap')]
def get_zodiac_of_date(date):
    date_number = int("".join((str(date.date().month), '%02d' % date.date().day)))
    for z in zodiacs:
        if date_number <= z[0]:
            return z[1]


# In[5]:


df["date_birthday"] = pd.to_datetime(df["date"] + " 2000")


# In[6]:


df["sign"] = df["date_birthday"].map(get_zodiac_of_date)


# In[7]:


df.head()


# In[8]:


df["count"] = 1
df["sign"].value_counts()


# In[9]:


df.groupby(["Year", "sign"]).sum().sort_values("count", ascending = False)["count"].head(30).plot.barh(figsize = (5, 10))


# In[10]:


dated = df.groupby("date_birthday").sum()
# dated["smoothed"]  = kalfil(dated["count"])


# In[11]:


# dated[["count", "smoothed"]].plot()


# ## Process
# 
# * keyword extraction
# * feature encoding
# * train test split
# * downsampling
# * gridsearch training optimisation
# * save model
# * parameter extraction
# * manual analysis 
#     * word clouds
#     * 

# In[12]:


# df = df.sample(100)


# In[13]:


from gensim.summarization import keywords
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
stop_words = get_stop_words('en')


# In[14]:


[x for x in nlp(" ".join(df["summary"][0].split(" ")[:100])) if x.pos_ == "ADJ"]


# In[15]:


x = " ".join(df["summary"][0].split(" ")[:100])


# In[16]:


x


# In[17]:


" ".join([y.text for y in nlp(x) if y.pos_ == "ADJ"])


# In[18]:


def extract_adjectives(x): 
    return " ".join([z.text for z in nlp(x) if z.pos_ == "ADJ"])


# In[19]:


def parall_extract(df): 
    df["adj"] = df["summary"].map(extract_adjectives)


# In[35]:


from multiprocessing import Pool

def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


# In[ ]:
print("extracting adjectives")

df = parallelize_dataframe(df, parall_extract, n_cores = 4)
print("finished extracting adjectives")

# In[ ]:


# text = ""
# for x in df["summary"]: 
#     text += x


# In[ ]:


def extract_keywords(x):
    return keywords(x).replace("\n", ", ")

# df["keywords"] = df["summary"].map(extract_keywords)


# In[ ]:

print("vectorising")
cv=CountVectorizer(max_df=0.65,stop_words=stop_words,max_features=2000)
word_count_vector=cv.fit_transform(df["adj"])
print("finished vectorising")

# In[ ]:


print(dir(cv))
cv.get_feature_names


# In[ ]:

print("building feature df")
features = pd.DataFrame(word_count_vector.todense(), columns = cv.get_feature_names())
features.to_csv("features.csv")
print("saved feature df")

# In[ ]:


print("done")


# In[ ]:


df.head()


# In[ ]:

print("factorising target")
df["target"],  key = pd.factorize(df["sign"])


# In[ ]:





# In[ ]:


df["target"].value_counts()


# In[ ]:

print("saving df")
df.to_excel("preped_target.xlsx")


# In[ ]:




