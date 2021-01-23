import csv
from datetime import datetime
import re
import requests 
from bs4 import BeautifulSoup

def get_url(position, location):
    """ generate the url from position and location"""
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location) # this will give the url including position location
    return url

def get_record(card):
    atag = card.h2.a # selecting the first a in first h2 tag inside a card
    job_title = atag.get('title') # getting the card job title property of a tag
    job_url = 'https://www.indeed.com' + atag.get('href')
    company = card.find('span', 'company').text.strip() # finding span with class company inside a card getting only the text not whole tag

    #location is in div tag with class recJobLoc and inside that a property name data-rc-loc
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')

    job_summary = card.find('div', 'summary').text.strip() # get the job summary
    post_date = card.find('span', 'date').text.strip()
    today = datetime.today().strftime('%Y-%m-%d')
    try: 
        job_salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        job_salary = ''
    record = (job_title, company, job_location, post_date, today, job_summary, job_salary, job_url)
    return record

def main(position, location):
    records = []
    url = get_url(position, location)
    while True: 
        response = requests.get(url) # it will return the response object of the URL
        soup = BeautifulSoup(response.text, 'html.parser') # this will rearrange the response acc to the html tags
        cards = soup.find_all('div', 'jobsearch-SerpJobCard') # this will find all the div tag with mentioned class

        for card in cards:
            record = get_record(card)
            records.append(record)
        try: 
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    #save the job data
    with open('results.csv', 'w', newline='', encoding ='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['jobTitle', 'Compnay', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary', 'JobUrl'])
        writer.writerows(records)

main('Software Developer', 'India')