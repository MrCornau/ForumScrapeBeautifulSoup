
from bs4 import BeautifulSoup
import requests
import csv
import json
import time
import random

data = {}
writedata = {}


# use beautifulsoup to access the html data from a given link
def getdata(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


# use pagination buttons to get the link of the next page
def getnextpage(soup):
    page = soup.find('ul', class_='ipsPagination')
    try:
        if not page.find('li', {'class': 'ipsPagination_next ipsPagination_inactive'}):
            url = str(
                page.find('li', {'class': 'ipsPagination_next'}).find('a')['href'])
            return url
        else:
            return
    except Exception as e:
        return


# extract specific comment features from the given html data
def crawlcomments(soup, idx, idx2, url):
    # use lambda to find all comments on a page
    for article in soup.find_all('article', id=lambda x: x and x.startswith('elComment_')):
        # feature 1: author
        authorRaw = article.find(
            'aside', class_='ipsComment_author').h3.text.strip()
        author = " ".join(authorRaw.split())  # remove whitespace
        try:  # feature 2: count of posts
            postRaw = article.find('aside', class_='ipsComment_author').ul.find(
                'li', attrs={'data-role': 'posts'}).text.strip()
            posts = " ".join(postRaw.split())  # remove whitespace
        except Exception as e:
            posts = None
        try:  # feature 3: Link to post
            link = article.find(
                'div', class_='ipsType_reset').find('a')['href'].replace('?do', '?tab')
        except Exception as e:
            link = None
        try:  # feature 4: Likes per post
            likes = article.find(
                'li', class_='ipsReact_reactCount').find_all('span')[1].text.lstrip().rstrip()
        except Exception as e:
            likes = None
        try:  # feature 5: date of post
            date = article.find(
                'div', class_='ipsColumn').find('time')['title']
        except Exception as e:
            date = None

        try:
            # feature 6: content
            contentRaw = article.find(
                'div', attrs={'data-role': 'commentContent'}).text.strip()
            noWhitespace = " ".join(contentRaw.split())
            # remove unnecessary content from posts
            newstring = noWhitespace.replace(
                'Hello guest! Please register or sign in to view the hidden content.', '--img--')
            newstring = newstring.replace(
                'Advertisement (gone after registration)', '')
            content = newstring.replace(
                'Hallo Gast! Du willst die Bilder sehen? Einfach registrieren oder anmelden!', '')
            thread = link.replace(
                'https://www.l-camera-forum.com/topic/', '').split("/")[0]
            newlink = str(url.split("?")[0] + link.replace(
                'https://www.l-camera-forum.com/topic/', '').split("/")[1]).replace('#comments', '').replace('findComment', 'comments').replace('&comment=', '#comment-')
        except Exception as e:
            content = None

        # append comment to a nested data format
        writedata['Threads'][idx2]['SubThreads'][idx]['comments'].append({
            'autor:': author,
            'posts': posts,
            'date': date,
            'content': content,
            'score': likes,
            'link': newlink,
            'thread': thread
        })
        # append comment to a plain comment list.
        comments.append({
            'autor:': author,
            'posts': posts,
            'date': date,
            'content': content,
            'score': likes,
            'link': newlink,
            'thread': thread
        })


# use html data to extract comments
def crawlTread(url, idx, idx2):
    currenturl = url
    writedata['Threads'][idx2]['SubThreads'][idx]['comments'] = []
    while True:
        soup = getdata(currenturl)
        crawlcomments(soup, idx, idx2, currenturl)

        # save all recently scraped comments to the disk, in case something is interupting the process, the site has not to be scraped from the beginning
        with open('ScrapeFiles/02-L-Forum-SubThreads_en.json', 'w') as outfile:
            json.dump(comments, outfile)
        # check how many comments are scraped from each subthread, break if more than 300
        if len(writedata['Threads'][idx2]['SubThreads'][idx]['comments']) < 300:
            currenturl = getnextpage(soup)
        else:
            return


# use the file generated in 02_CrawlSubthreads.py to extract comments
with open('ScrapeFiles/02-L-Forum-SubThreads_en.json') as json_file:
    data = json.load(json_file)
    comments = []  # Array to store all comments in
    writedata = data  # duplicate Data for further preceding
    for idx2, thread in enumerate(data['Threads']):
        try:
            for idx, subthread in enumerate(thread['SubThreads']):
                url = subthread['link']
                crawlTread(url, idx, idx2)
                print(idx2, idx, thread['title'], subthread['title'])
        except Exception as e:
            print(thread, e)
    with open('ScrapeFiles/03-L-Forum_BD_en.json', 'w') as outfile:
        json.dump(comments, outfile)
