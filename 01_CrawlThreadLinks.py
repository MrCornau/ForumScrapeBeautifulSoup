
from bs4 import BeautifulSoup
import requests
import csv
import json


# requests HTML Code from given URL
def getData(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup

# Search for Threads on given URL


def getLinks(soup):
    Threads = {}
    Threads['Threads'] = []

    # Find section with english Threads
    section = soup.section.find('ol', {'class': 'ipsDataList'})
    # Find list of threads
    for Thread in section.find_all('li', {'class': 'cForumRow'}):
        try:
            # Find the Threadlist - every thread has multiple subthreads
            ThreadList = Thread.find('ul', {'class': 'ipsDataItem_subList'})
        except Exception as e:
            ThreadList = None
            print(e, 'error')
            return
        if ThreadList != None:
            # get link and title from all subthreads and store them to the Threads Array
            for Item in ThreadList.find_all('li'):
                link = Item.find('a')['href']
                title = Item.find('a').text
                Threads['Threads'].append({
                    'link': link,
                    'title': title
                })
        else:
            print('error', Thread)
    return Threads


url = 'https://www.l-camera-forum.com/index.php'  # Page to Scrape

# call getLinks after calling getData
Outfile_Data = getLinks(getData(url))

# store all Threads in an json file to continue working. Use this file in 02_CrawlSubthreads.py
with open('FileName.json', 'w') as outfile:
    json.dump(Outfile_Data, outfile)
