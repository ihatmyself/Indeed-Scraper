import requests
from bs4 import BeautifulSoup
import pandas as pd

#api_link = ''
#api_link =  "https://app.scrapingbee.com/api/v1/store/google?api_key=55ML1HZJH7UP7BITWC0PIU5NUNG86XAE6I2DF066R3AITKQSCW0ALE1NJR2IE6PA5NTG28346C2CID9X&search="
#api_link = 'https://api.scrapingdog.com/scrape?api_key=648b01e6c2270964d0eb0f78&url='
#api_link = 'http://api.scrape.do?token=ae6fc2d34a9f4aae87559c721bda1fe90bd5c08823f&url='
api_link = 'http://api.scraperapi.com?api_key=36e080cac88bbe9196c6fcf16597f494&url='
max_page = 10
today = "2023-07-20"

def get_url(position, location):
    template = api_link + 'https://www.indeed.com/jobs?q={}&l={}'
    #"http://api.scraperapi.com?api_key=f6d45677ae103feaa7f556a76740f89c&url=https://www.indeed.com/jobs?q={}&l={}"

    position = position.replace(" ","+")
    location = location.replace(" ","+")
    url = template.format(position,location)
    return url


def get_record(card):

    try:
        job_title = card.h2.a.get('aria-label').replace("full details of ","")
    except:
        None
   
    print(job_title)

    job_url = 'https://www.indeed.com' + card.h2.a.get('href')

    #print(job_url)
    try:
        company = card.find("div",{"class":"companyInfo"}).find("span",{"class":"companyName"}).text
    except:
        company = None

    print(company)
    try:
        job_location = card.find("div",{"class":"companyInfo"}).find('div',{'class':'companyLocation'}).text
    except:
        job_location = None

    #print(job_location)
    try:
        post_date = card.find('table',{'class':'jobCardShelfContainer'}).find('span',{'class':'date'}).text.replace("PostedPosted","Posted")
    
    except:
        post_date = None

    try:
        salary = card.find('div',{'class':'attribute_snippet'}).text

    except:
        salary = None

    record = (job_title, company, job_location, post_date, salary, job_url)
    return(record)

def create_descriptions(df):

    job_links = df['job_url']
    job_description_elements = [ ]
    print(job_links)
    count = 1
    for job_link in job_links:
        url = api_link + job_link

        job_description_element = "none"

        try:
            response = requests.get(url, timeout=20)  # Set timeout to 20 seconds.
            print(count, url, "The response is", response.status_code)
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"{count}{e}. Skipping to next URL.")
            job_description_element = "N/A"
        else:
            soup = BeautifulSoup(response.text, "html.parser")

            try:
                job_description_element = soup.find('div', {'class':'jobsearch-jobDescriptionText'}).text.strip()
                print(count , "success")
            except:
                job_description_element = "N/A"
                print(count , "cannot find the job description")
    

        job_description_elements.append(job_description_element)
        count += 1

    df['job_description'] = job_description_elements

    return df



def main(position, location):

    records = [ ]
    url = get_url(position, location)
    print(url)
    page = 0
    total_cards = 0

    while page < max_page:
        response = requests.get(url)
        print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', {'class': 'cardOutline'})           

        for card in cards:
            record = get_record(card)
            records.append(record)
        
        total_cards += len(cards)
        
        try:
            url = api_link + 'https://www.indeed.com' + soup.find('nav',{'role':'navigation'}).find('a', {'aria-label': 'Next Page'}).get('href')

            print(url)
            
        except AttributeError:

            print("Done. Terminating the loop")

            break

        page += 1
            
    df = pd.DataFrame(records, columns=['job_title', 'company', 'job_location', 'post_date', 'salary', 'job_url'])

    print(f'The total number of postings is {total_cards}')

    create_descriptions(df)

    filename = f'{position.replace(" ", "_")}@{location.replace(" ", "_")}#{today}.csv'

    #df.to_csv(os.path.join(directory, filename), index=False)

    df.to_csv(filename,index=False)

main('data scientist','dallas')