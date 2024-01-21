import requests
from bs4 import BeautifulSoup
import csv
import time

def get_url(position, location):
    template = 'https://api.scrapingdog.com/scrape?api_key=648b01e6c2270964d0eb0f78&url=https://www.indeed.com/jobs?q={}&l={}&dynamic=false'
    position = position.replace(" ","+")
    location = location.replace(" ","+")
    url = template.format(position,location)
    return url


def get_record(card):

    job_title = card.h2.a.get('aria-label').replace("full details of ","")

    #print(job_title)

    job_url = 'https://www.indeed.com' + card.h2.a.get('href')

    #print(job_url)

    company = card.find("div",{"class":"companyInfo"}).find("span",{"class":"companyName"}).text

    print(company)

    job_location = card.find("div",{"class":"companyInfo"}).find('div',{'class':'companyLocation'}).text

    #print(job_location)
    try:
        post_date = card.find('table',{'class':'jobCardShelfContainer'}).find('span',{'class':'date'}).text.replace("PostedPosted","Posted")

    except:
        post_date = None
    #print(post_date)

    record = (job_title, company, job_location, post_date, job_url)
    return(record)

def main(position, location):

    records = [ ]
    url = get_url(position, location)
    count = 0

    while count < 10:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', {'class': 'cardOutline'})           

        for card in cards:
            record = get_record(card)
            records.append(record) 
        
        try:
            url = 'https://api.scrapingdog.com/scrape?api_key=648b01e6c2270964d0eb0f78&url=https://www.indeed.com' + soup.find('nav',{'role':'navigation'}).find('a', {'aria-label': 'Next Page'}).get('href') + '&dynamic=false'

            print(url)
            
        except AttributeError:
            print("Done. Terminating the loop")
            break

        time.sleep(1)
        count =+ 1

    '''while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', {'class': 'cardOutline'})           
       
        for card in cards:
            record = get_record(card)
            records.append(record) 
            
        try:
            url = 'https://api.scrapingdog.com/scrape?api_key=648b01e6c2270964d0eb0f78&url=https://www.indeed.com' + soup.find('nav',{'role':'navigation'}).find('a', {'aria-label': 'Next Page'}).get('href') + '&dynamic=false'

            print(url)
        
        except AttributeError:
            
            break

        time.sleep(1)'''
            
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        
        writer = csv.writer(f)
        writer.writerow(['job_title', 'company', 'job_location', 'post_date', 'job_url'])
        writer.writerows(records)

main("data scientist intern","")