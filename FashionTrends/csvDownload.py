# coding=UTF-8
import urllib.request
import csv
import os
from urllib.parse import urlparse
import shutil
import glob

image_dir = 'C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/'

current_images = glob.glob('C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/*.jpg')
with open('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/dresses.csv', newline='\n') as file:
   reader = csv.reader(file, delimiter=',')
   for row in reader:
      if '\\' not in row[0].split("\'")[1] and image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg') not in current_images: #Skip non-ascii characters - ChicTopia just fails to use them as URLs for some reason
         with urllib.request.urlopen(row[0].split("\'")[1]) as response, open(image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            print(os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'))
current_images = glob.glob('C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/*.jpg')
with open('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/pants.csv', newline='\n') as file:
   reader = csv.reader(file, delimiter=',')
   for row in reader:
      if '\\' not in row[0].split("\'")[1] and image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg') not in current_images: #Skip non-ascii characters - ChicTopia just fails to use them as URLs for some reason
         with urllib.request.urlopen(row[0].split("\'")[1]) as response, open(image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            print(os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'))
current_images = glob.glob('C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/*.jpg')
with open('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/skirts.csv', newline='\n') as file:
   reader = csv.reader(file, delimiter=',')
   for row in reader:
      if '\\' not in row[0].split("\'")[1] and image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg') not in current_images: #Skip non-ascii characters - ChicTopia just fails to use them as URLs for some reason
         with urllib.request.urlopen(row[0].split("\'")[1]) as response, open(image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            print(os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'))
current_images = glob.glob('C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/*.jpg')
with open('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/shirts.csv', newline='\n') as file:
   reader = csv.reader(file, delimiter=',')
   for row in reader:
      if '\\' not in row[0].split("\'")[1] and image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg') not in current_images: #Skip non-ascii characters - ChicTopia just fails to use them as URLs for some reason
         with urllib.request.urlopen(row[0].split("\'")[1]) as response, open(image_dir + os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            print(os.path.basename(urlparse(row[0].split("\'")[1]).path).replace('.jpg', row[1] + '.jpg'))
'''
try:
   os.path.basename(urlparse(row[1]).path).encode('ascii')
except UnicodeEncodeError:
   pass  # string is not ascii
else:
   with urllib.request.urlopen(row[1]) as response, open(image_dir + os.path.basename(urlparse(row[1]).path), 'wb') as out_file:
      shutil.copyfileobj(response, out_file)
      print(os.path.basename(urlparse(row[1]).path))
   pass  # string is ascii
'''