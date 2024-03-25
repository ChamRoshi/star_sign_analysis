#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import wikipedia
from multiprocessing import Pool


def test(): 
    celeb = "Heinrich Georg Bronn, German geologist and paleontologist (d. 1862)"
    page = wikipedia.page(celeb)
    page.url

    print(page.summary.split("(")[1].split(" – ")[0])

def get_data(celeb): 
    page = wikipedia.page(celeb)
    page.url
    date = page.summary.split("(")[1].split(" – ")[0] 
    content = page.content
    return date, content


# In[ ]:


def mp_get_data(celeb): 
    try:
        page = wikipedia.page(celeb)
        page.url
        # date = page.summary.split("(")[1].split(" – ")[0] 
        date = ""
        content = page.content
        returnr = {"celeb": celeb, "date": date, "content": content}
        return returnr
    except Exception as e: 
        print(e)
        pass


if __name__ == "__main__":
    df = pd.read_csv("famous_births.csv")
    print(df.head())


#     dates = []
#     summaries = []
#     for num, celeb in enumerate(df["Name"]): 
#         if num%500 == 0: 
#             print(num)


#         try:
#             d, c = get_data(celeb)
#         except: 
#             d = ""
#             c = ""
#         dates.append(d)
#         summaries.append(c)
    
    processes = 30
    p = Pool(processes)
    
    res = p.map(mp_get_data, df["Name"])
    
    dates = {}
    for x in res: 
        try: 
            dates[x["celeb"]] = x["date"]
        except Exception as e: 
            print(e)
            pass
        
    summaries = {}
    for x in res: 
        try: 
            summaries[x["celeb"]] = x["content"]
        except Exception as e: 
            print(e)
            pass
            
    df["birthday"] = df["Name"].map(dates)
    df["summary"] = df["Name"].map(summaries)
    df.dropna().to_excel("dated_births.xlsx")