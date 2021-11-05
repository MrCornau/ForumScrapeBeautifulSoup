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







