import requests
from bs4 import BeautifulSoup
import pandas as pd

def create_descriptions(df):
    
    job_links = df['job_url']
    job_description_elements = [ ]
    print(job_links)
    count = 1
    for job_link in job_links:

        url = "https://api.scrapingdog.com/scrape?api_key=648b01e6c2270964d0eb0f78&url=" + job_link + "&dynamic=false"
        response = requests.get(url)
        print(count,url,"n/The response is",response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        print(count,"Done parsing")

        try:
            job_description_element = soup.find('div', {'class':'jobsearch-jobDescriptionText'}).text.strip()
            print(count , "success")
        except:
            job_description_element = "none"
            print(count , "failure")

        job_description_elements.append(job_description_element)

        count += 1

    df['job_description'] = job_description_elements

    df.to_csv('updated_results.csv', index=False)

    print("loop done")
