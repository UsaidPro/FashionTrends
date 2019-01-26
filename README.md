This repository contains my work for team Maverick in DSC at University of Texas at Dallas. All code contained in this repository is my own (excluding libraries). I plan to halt this project for a while (since team members have all quit due to lack of time) and might revisit it during the summer. I have now posted it on Github with public permissions so that others may benefit.

# FashionTrends
This project is an effort to predict fashion trends over time using machine learning. Currently, I am able to classify different types of clothing (Shirts, Skirts, Pants, Dress) using images webscraped from chictopia.com and training a model built using Keras.

How could this project be useful? Being able to predict fashion trends would allow retailers to better their logistics for storage/shipping of clothes. Right now, retailers use sales along with results from fashion shows/blogs to determine what clothes would be useful for fashion. This project _could_ add a new dimension of analytics for such retailers (being able to use social media to predict demand possibly).

## How is this project set up
Currently, this project is split into several files to make prototyping easier. Current workflow:

`webscraper.py --> csvDownload.py --> preprocessing.py --> FashionTrends.py`

`webscraper.py` webscrapes chictopia.com for images and tags. `csvDownload.py` actually downloads the scraped images which are fed into `preprocessing.py` to perform image preprocessing. Finally, `FashionTrends.py` is run to actually train the model.

## Details on how it works
I use [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to parse webpages. Then, I download the images and start preprocessing.

### Preprocessing
If `preprocessing.py` started with this image:

![Original Image](/imgs/original.jpg "Original Image")

I remove the background (everything but humans) using [DeepLabv3+](https://github.com/bonlime/keras-deeplab-v3-plus).

![Removed Background](/imgs/removed.jpg "Removed Background")

After removing the background, I then resize the image and perform k-means clustering using [KMeans from Scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html). Number of clusters currently is 4.

![Resized and Clustered](/imgs/128size.jpg "Resized and Clustered")

Finally, I save the resized image along with a 2D NumPy array where each 2D location is the corresponding cluster value at that location based on cluster size and starting at 0 for largest cluster. This is then used for training.

### Training
`FashionTrends.py` first creates a pandas dataset using the CSVs from `webscraping.py` and then constructs a 3D numpy array of the arrays created from `preprocessing.py`. After this, training occurs.

My current model is a CNN with 2 convolutional layers and 2 dropout layers followed by a softmax layer. Optimizer is Adadelta. For specifics, look at (/FashionTrends/FashionTrends.py#L99).

Result after training:

![Results](/imgs/result.jpeg "Results")

These results are pretty good considering a small and potentially noisy dataset (~1200 images). For further improvements, I might use a GAN (Generational-Adversarial Network) which has been proven to do better for fashion classification and add more images to the dataset.

**Disclaimer:** I am _not_ a professional (yet). For any other newbies who stumble upon this repository, don't treat these results as guarenteed good nor the methodology I used - there might be better alternatives I just don't have experience in yet.
