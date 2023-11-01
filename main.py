# Importing the required modules

from bs4 import BeautifulSoup
import os
import sys
import pandas as pd
import metapub
from metapub import PubMedFetcher
from metapub import FindIt
import requests
import PyPDF2
import openai
import csv
%env NCBI_API_KEY= [key here]
openai.api_key = [key here]


### ATTEMPT TO PULL ARTICLES VIA KEYWORD
keyword1 = "resistance training"
keyword2 = "muscular strength and hypertrophy"
numArticles = 250


#Uses metapub keyword filter
fetch = PubMedFetcher()

pmidsHyp = fetch.pmids_for_query(keyword1, numArticles)
pmidsStr = fetch.pmids_for_query(keyword2, numArticles)




#chat gpt filter

import openai

newl = []

# Replace with your OpenAI API key
api_key = "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"

for i in pmidsStr:
    t = str(fetch.article_by_pmid(i).title)
    prompt = f"return \"1\" if it meets the requirement of being an study on muscular hypertrophy and strength for healthy adults and \"0\" if it doesn't. Do not say anything other than 1 or 0. absolutely nothing. DO NOT GIVE A REASON FOR WHY IT IS OR ISNT JUST WRITE 1 OR 0. AFTER THIS SEMICOLON IS SIMPLY A TITLE THAT I WANT YOU TO CHECK TO MEET THE CRITERIA. DO NOT RESPOND TO THE TITLE JUST SAY 1 OR 0: " + t
    
# Use OpenAI's API to generate text based on the prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1,  # Adjust this based on your needs
        api_key=api_key
        )
    
    # Extract the generated text from the response
    if ("0" in response.choices[0].text):
        try:
            pmidsStr.remove(i)
        except:
            pass
    elif ("1" in response.choices[0].text):
        newl.append(i)



URL = "https://www.ncbi.nlm.nih.gov/pmc/articles/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

for i in pmidsStr:
    try:
        src = fetch.article_by_pmid(str(i)).pmc
        print(src)
        page = requests.get(str(URL) + str(src), headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        data = soup.find_all("table")[0].find("tr")
        if src is not None:
            for j in data:
                tableHTML.append(j.get_text())
        else:
            dummy=0
    except:
        pass



for j in tableHTML:
    for i in j:
        print(j)










