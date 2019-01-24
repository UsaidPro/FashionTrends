"""
Scrapes ChicTopia.com's webpages to generate preliminary dataset of different clothing items
"""
import urllib3
from bs4 import BeautifulSoup
import csv

http = urllib3.PoolManager()

"""
Parses ChicTopia page to get possibly valuable information
"""
def parsePage(url):
   page = http.request('GET', url)
   soup = BeautifulSoup(page.data)
   dateText = ''
   userText = ''
   descText = ''
   print("URL:")
   url = soup.find('div', attrs = {'id':'image_wrap'}).find('img')['src']
   print(url)
   print("DATE:")
   date = soup.find('meta', attrs = {'itemprop':'dateCreated'})
   if date is not None:
      print(date['content'])
      dateText = date['content']
   print("USER:")
   user = soup.find('div', attrs={'class':'nocap'}).find('a', href=True)
   if user is not None:
      print(user.text)
      userText = user.text
   tags = soup.find('div', attrs={'id':'tag_boxes'}).findAll('a')
   print("TAGS:")
   tagStr = ''
   for tag in tags:
      print(tag.text)
      tagStr += tag.text + ';'
   print("DESCRIPTION:")
   desc = soup.find('div', attrs={'id':'photo_description'}).find('p')
   if desc is not None:
      print(desc.text)
      descText = desc.text
   clothingTags = soup.find('div', attrs = {'class':'garmentLinks'}).findAll('a', href=True, recursive=False) #Can remove the if check if this works
   color = ''
   type = ''
   clothingStr = ''
   for tag in clothingTags:
      if '/color' in tag['href']:
         color += tag.text
      if tag.has_attr('class'):
         type += tag.text
         clothingStr += color + ':' + type + ';'
         color = ''
         type = ''
   return (url.encode('utf-8'), dateText, userText.encode('utf-8'), tagStr.encode('utf-8'), descText.encode('utf-8'), clothingStr.encode('utf-8'))

#Scrape ChicTopia for shirts
url = 'http://chictopia.com/Shirt/info'
pageIndex = 1
lastPage = 40
#Remember to change the file too!
with open('shirts.csv', mode='w') as file:
   writer = csv.writer(file, delimiter=',', lineterminator='\n')
   for index in range(pageIndex, lastPage + 1):
      page = http.request('GET', url + '/' + str(index))
      soup = BeautifulSoup(page.data)
      imageTile = soup.findAll('div', attrs={'class':'photo_hover'})
      for tile in imageTile:
         link = tile.findAll("a", recursive=False)[0]
         if link.has_attr('href'):
            data = parsePage('http://chictopia.com' + link['href'])
            writer.writerow(data)
#Scrape ChicTopia for skirts
url = 'http://chictopia.com/Skirt/info'
with open('skirts.csv', mode='w') as file:
   writer = csv.writer(file, delimiter=',', lineterminator='\n')
   for index in range(pageIndex, lastPage + 1):
      page = http.request('GET', url + '/' + str(index))
      soup = BeautifulSoup(page.data)
      imageTile = soup.findAll('div', attrs={'class':'photo_hover'})
      for tile in imageTile:
         link = tile.findAll("a", recursive=False)[0]
         if link.has_attr('href'):
            data = parsePage('http://chictopia.com' + link['href'])
            writer.writerow(data)
#Scrape ChicTopia for pants
url = 'http://chictopia.com/Pant/info'
with open('pants.csv', mode='w') as file:
   writer = csv.writer(file, delimiter=',', lineterminator='\n')
   for index in range(pageIndex, lastPage + 1):
      page = http.request('GET', url + '/' + str(index))
      soup = BeautifulSoup(page.data)
      imageTile = soup.findAll('div', attrs={'class':'photo_hover'})
      for tile in imageTile:
         link = tile.findAll("a", recursive=False)[0]
         if link.has_attr('href'):
            data = parsePage('http://chictopia.com' + link['href'])
            writer.writerow(data)
#Scrape ChicTopia for dresses
url = 'http://chictopia.com/Dress/info'
with open('dresses.csv', mode='w') as file:
   writer = csv.writer(file, delimiter=',', lineterminator='\n')
   for index in range(pageIndex, lastPage + 1):
      page = http.request('GET', url + '/' + str(index))
      soup = BeautifulSoup(page.data)
      imageTile = soup.findAll('div', attrs={'class':'photo_hover'})
      for tile in imageTile:
         link = tile.findAll("a", recursive=False)[0]
         if link.has_attr('href'):
            data = parsePage('http://chictopia.com' + link['href'])
            writer.writerow(data)