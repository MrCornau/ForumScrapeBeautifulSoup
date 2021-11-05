from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://coreyms.com/').text


soup = BeautifulSoup(source, 'lxml')

article = soup.find('article')

# print (article.prettify())

csv_file = open('cms_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['headline','summary','video_link'])


for article in soup.find_all('article'):
    headline = article.h2.a.text
    print(headline)
    print()
    description = article.find('div',class_='entry-content').p.text
    print(description)
    

    try: 
        videourl = article.find('iframe', class_='youtube-player')['src'].split('/')[4].split('?')[0]
        yt_link = f'https://youtube.com/watch?v={videourl}'
    except Exception as e:
        yt_link = None

    print(yt_link)
    print()
    print()

    csv_writer.writerow([headline,description,yt_link])


csv_file.close()









# source = requests.get('https://www.l-camera-forum.com/topic/325898-hypothetical-question-this-should-stir-the-pot/').text
# soup = BeautifulSoup(source, 'lxml')


# csv_file = open('leicaScrape2.csv', 'w')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Autor','Posts','Date','content'])



# for article in soup.find_all('article', id=lambda x: x and x.startswith('elComment_')):
#     autor = article.find('aside', class_='ipsComment_author').h3.text
#     print (autor)
#     try: 
#         posts = article.find('aside', class_='ipsComment_author').ul.find('li', attrs={'data-role' : 'posts'}).text
#     except Exception as e:
#         posts = None
#     print (posts)
#     try: 
#         date = article.find('div', class_='ipsColumn').find('time')['title']
#     except Exception as e:
#         date = None
#     if date!=None:
#         print (date)
#     try: 
#         content = article.find('div', attrs={'data-role' : 'commentContent'}).text
#     except Exception as e:
#         content = None
#     print (content)

#     csv_writer.writerow([autor,posts,date,content])


# csv_file.close()







