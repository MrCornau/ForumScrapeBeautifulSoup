
from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/').text


soup = BeautifulSoup(source, 'lxml')

csv_file = open('leicaScrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Autor','Posts','Date','content'])



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


csv_file.close()

# article2 = soup.find_all('form')
# .article.find('div', attrs={'data-role' : 'commentContent'})

# content = article.find('div').p

##print (article[0])




# for article in article.find_all('div', attrs={'data-role' : 'commentContent'}):
#     print(article.prettify())
#     print()
#     print('_________________clear___')
# comment = article.find('div', class_='cPost_contentWrap').find('p')

# autor = articleContent.find('div')


# # print (articleContent.prettify())
# print (autor)
##print (articleContent.p.next_sibling.next_sibling)
# csv_file.close()







