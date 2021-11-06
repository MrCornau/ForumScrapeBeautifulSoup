
from bs4 import BeautifulSoup
import requests
import csv
import json


suburl='https://www.l-camera-forum.com/forum/263-leica-m10/'
url = 'https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/'

SubsubLinks = {}
SubsubLinks['SubThreads'] = []

def getdata(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def getnextpage(soup):
    page = soup.find('ul', class_='ipsPagination')
    if not page.find('li', {'class' : 'ipsPagination_next ipsPagination_inactive'}):
        url = str(page.find('li', {'class' : 'ipsPagination_next'}).find('a')['href'])
        return url
    else:
        return


def crawlLinks(subsoup):
    for subsub in subsoup.find_all('li', {'class': 'ipsDataItem ipsDataItem_responsivePhoto'}):
        try: 
            link = subsub.find('a')['href']
            title = subsub.find('a').text.lstrip().rstrip() 
            time = subsub.find('time')['datetime']
            SubsubLinks['SubThreads'].append({
                'title': title,
                'link': link,
                'time': time
            })
        except Exception as e:
            link =  None
            title = None
            time = None
        finally:
            print(link,'__',title,'___',time)
        print('_______')
    
    with open('subsubTest.txt', 'w') as outfile:
        json.dump(SubsubLinks, outfile)


crawlLinks(getdata(suburl))

# while True:
#     subsoup = getdata(suburl);
#     crawlLinks(subsoup);
#     suburl = getnextpage(subsoup)
#     if not suburl:
#         print(SubsubLinks)
#         break








# source = requests.get('https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/').text
# soup = BeautifulSoup(source, 'lxml')





# 






