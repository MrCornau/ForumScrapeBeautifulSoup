
from bs4 import BeautifulSoup
import requests
import csv



suburl='https://www.l-camera-forum.com/forum/263-leica-m10/'
url = 'https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/'

SubsubLinks = []

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
    # print(subsoup.find('li', {'class': 'ipsDataItem'}).find('a')['href'])
    # link = subsoup.find('li', {'class': 'ipsDataItem'}).find('a')['href']
    # title = subsoup.find('li', {'class': 'ipsDataItem'}).find('a').text
    # time = subsoup.find('li', {'class': 'ipsDataItem'}).find('time')['datetime']
    # print(link,'__',title,'___',time)
    for subsub in subsoup.find_all('li', {'class': 'ipsDataItem ipsDataItem_responsivePhoto'}):
        try: 
            link = subsub.find('a')['href']
            title = subsub.find('a').text
            time = subsub.find('time')['datetime']
        except Exception as e:
            link =  'blaaa'
            title = 'bliii'
            time = 'blub'
        finally:
            print(link,'__',title,'___',time)

        print('_______')
    # time = subsoup.find('li', {'class': 'ipsDataItem'}).find('time')['datetime']


    #     SubsubLinks.append(subsub.find('a')['href'])



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






