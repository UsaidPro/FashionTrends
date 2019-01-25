This repository contains my work for team Maverick in DSC at University of Texas at Dallas. All code contained in this repository is my work.

# FashionTrends
This project is an effort to predict fashion trends over time using machine learning. Currently, I am able to classify different types of clothing (Shirts, Skirts, Pants, Dress) using images webscraped from chictopia.com and training a model built using Keras.

How could this project be useful? Being able to predict fashion trends would allow retailers to better their logistics for storage/shipping of clothes. Right now, retailers use sales along with results from fashion shows/blogs to determine what clothes would be useful for fashion. This project _could_ add a new dimension of analytics for such retailers (being able to use social media to predict demand possibly).

## How is this project set up
Currently, this project is split into several files to make prototyping easier. Current workflow:

`webscraper.py --> csvDownload.py --> preprocessing.py --> FashionTrends.py`

`webscraper.py` webscrapes chictopia.com for images and tags. `csvDownload.py` actually downloads the scraped images which are fed into `preprocessing.py` to perform image preprocessing. Finally, `FashionTrends.py` is run to actually train the model.

## Details on how it works
I use [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to parse webpages. Then, I download the images and start preprocessing.
