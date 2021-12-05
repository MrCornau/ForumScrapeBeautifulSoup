
from bs4 import BeautifulSoup
import requests
import json

data = {}


# use beautifulsoup to access the html data from a given link
def getdata(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


# use pagination buttons to get the link of the next page
def getnextpage(soup):
    page = soup.find('ul', class_='ipsPagination')
    try:
        # when the ipsPagination_inactive class is added to the Pagination item, we have reached the last page
        if not page.find('li', {'class': 'ipsPagination_next ipsPagination_inactive'}):
            url = str(
                page.find('li', {'class': 'ipsPagination_next'}).find('a')['href'])
            return url
        else:
            return
    except Exception as e:
        return


# Search in the html data for all links from subthreads
def crawlLinks(subsoup):
    for subsub in subsoup.find_all('li', {'class': 'ipsDataItem ipsDataItem_responsivePhoto'}):
        try:
            link = subsub.find('a')['href']
            title = subsub.find('a').text.lstrip().rstrip()
            time = subsub.find('time')['datetime']
            data['Threads'][idx]['SubThreads'].append({
                'title': title,
                'link': link,
                'time': time
            })
        except Exception as e:
            link = None
            title = None
            time = None


# access the html data, and call for the next page if it exists and if there are not more than 350 subthreads stored.
def crawlTread(url, idx):
    suburl = url
    # create new List for the following threads
    data['Threads'][idx]['SubThreads'] = []
    while True:
        subsoup = getdata(suburl)  # scrape page from given url
        # search in html code for the links of the subthread
        crawlLinks(subsoup)
        suburl = getnextpage(subsoup)
        # we decided to limit it to 350 subthreads per thread
        if len(data['Threads'][idx]['SubThreads']) > 350 or not suburl:
            return


# Use the file which was created from 01_CrawlThreads.py to extend it with avaiable subthreads
with open('ScrapeFiles/01-L-Forum-Threads_en.json') as json_file:
    data = json.load(json_file)
    for idx, thread in enumerate(data['Threads']):
        url = thread['link']
        crawlTread(url, idx)
        with open('AllThreadLInks_New.txt', 'w') as outfile:
            json.dump(data, outfile)
            print(len(data['Threads']))

    with open('ScrapeFiles/02-L-Forum-SubThreads_en.json', 'w') as outfile:
        json.dump(data, outfile)
