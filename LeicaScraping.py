
from bs4 import BeautifulSoup
import requests
import csv


url = 'https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/'

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




def crawlcomments(soup):
    for article in soup.find_all('article', id=lambda x: x and x.startswith('elComment_')):
        autor = article.find('aside', class_='ipsComment_author').h3.text
        print (autor)
        try: 
            posts = article.find('aside', class_='ipsComment_author').ul.find('li', attrs={'data-role' : 'posts'}).text
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
            content = article.find('div', attrs={'data-role' : 'commentContent'}).text
        except Exception as e:
            content = None
        print (content)

        csv_writer.writerow([autor,posts,date,content])


csv_file = open('leicaScrape2.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Autor','Posts','Date','content'])





while True:
    soup = getdata(url)
    crawlcomments(soup)
    url = getnextpage(soup)
    if not url:
        csv_file.close()
        break

    print(url)






# source = requests.get('https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/').text
# soup = BeautifulSoup(source, 'lxml')





# 






