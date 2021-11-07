
from bs4 import BeautifulSoup
import requests
import csv
import json
import time
import random

data = {}



def getdata(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def getnextpage(soup):
    page = soup.find('ul', class_='ipsPagination')
    try: 
        if not page.find('li', {'class' : 'ipsPagination_next ipsPagination_inactive'}):
            url = str(page.find('li', {'class' : 'ipsPagination_next'}).find('a')['href'])
            return url
        else:
            return
    except Exception as e:
            return



def crawlcomments(soup,idx):
    for article in soup.find_all('article', id=lambda x: x and x.startswith('elComment_')):
        autor = article.find('aside', class_='ipsComment_author').h3.text.lstrip().rstrip() 
        print (autor)
        try: 
            posts = article.find('aside', class_='ipsComment_author').ul.find('li', attrs={'data-role' : 'posts'}).text.lstrip().rstrip() 
        except Exception as e:
            posts = None
        print (posts)
        try: 
            date = article.find('div', class_='ipsColumn').find('time')['title']
        except Exception as e:
            date = None
        if date!=None:
            print (date)
        try: 
            content = article.find('div', attrs={'data-role' : 'commentContent'}).text.lstrip().rstrip() 
        except Exception as e:
            content = None
        print (content)
        data['SubThreads'][idx]['comments'].append({
        'autor:':autor,
        'posts':posts,
        'date':date,
        'content':content}) 

      




def crawlTread(url,idx):
    currenturl = url
    data['SubThreads'][idx]['comments'] = []
    while True:
        soup = getdata(currenturl)
        crawlcomments(soup,idx)
        currenturl = getnextpage(soup)
        if len(data['SubThreads'][idx]['comments'])> 200 or not currenturl:
            print('Thread Nr:', idx)
            break




with open('LeicaM240262.txt') as json_file:
    data = json.load(json_file)
    print(len(data['SubThreads']))
    data['SubThreads'][0]['comments'] = []
    data['SubThreads'][0]['comments'].append({
        'comment':'comment'
    })
    i=0
    for idx, thred in enumerate(data['SubThreads']):
        url = thred['link']
        crawlTread(url,idx)
        time.sleep(random.randrange(10,20))
        if idx > 500:
            break
    
    print('______done______')
    with open('LeicaM240262_Run.txt', 'w') as outfile:
        json.dump(data, outfile)


