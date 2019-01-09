import pandas as pd
import numpy as np
import os


cols = ['URL', 'Date', 'User', 'Tags', 'Description', 'Clothing']
dresses = pd.read_csv('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/dresses.csv', header=None)
dresses.columns = cols
dresses['Dress'] = True
pants = pd.read_csv('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/pants.csv', header=None)
pants.columns = cols
pants['Pant'] = True
skirts = pd.read_csv('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/skirts.csv', header=None)
skirts.columns = cols
skirts['Skirt'] = True
shirts = pd.read_csv('C:/Users/usaid/Documents/Visual Studio 2015/Projects/FashionTrends/FashionTrends/shirts.csv', header=None)
shirts.columns = cols
shirts['Shirt'] = True
dataset = pd.concat([dresses, pants, skirts, shirts])

def clean(string):
   return string.split('\'')[1]

#dataset.columns = ['URL', 'Date', 'User', 'Tags', 'Description', 'Clothing']
dataset['URL'] = dataset['URL'].apply(clean)
dataset['Img'] = dataset['URL'].apply(lambda x: os.path.basename(x).replace('.jpg', ''))
dataset['File'] = dataset['Img'] + dataset['Date']
dataset['User'] = dataset['User'].apply(clean)
dataset['Tags'] = dataset['Tags'].apply(clean)
dataset['Description'] = dataset['Description'].apply(clean)
dataset['Clothing'] = dataset['Clothing'].apply(clean)

#Determine whether image has extra clothing or not - this might/might not improve accuracy since we can classify shirt/pant rather than just shirt or just pant
#However, it might be easier to instead ignore shirts, since having a skirt and a dress is unlikely (?)
dataset['Dress'] = dataset['Clothing'].str.contains('dress', na=False, regex=True) | dataset['Description'].str.contains('dress', na=False, regex=True) | dataset['Dress']
dataset['Pant'] = dataset['Clothing'].str.contains('pant', na=False, regex=True) | dataset['Description'].str.contains('pant', na=False, regex=True) | dataset['Pant']
dataset['Skirt'] = dataset['Clothing'].str.contains('skirt', na=False, regex=True) | dataset['Description'].str.contains('skirt', na=False, regex=True) | dataset['Skirt']
dataset['Shirt'] = dataset['Clothing'].str.contains('shirt', na=False, regex=True) | dataset['Description'].str.contains('shirt', na=False, regex=True) | dataset['Shirt']

#y is now dataset['Pant'], dataset['Dress'], dataset['Skirt'] and dataset['Shirt']

#Load cluster dataset
clustered = np.load("C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/Clustered/Clustered.zip")

print(dataset.shape)
print(dataset['Img'].head())
dataset = dataset[dataset['File'].isin(clustered.files)]

print(dataset.shape)
#print(clusters.shape)
#print(headers.shape)
print(dataset.nunique())

#Drop duplicate images, making sure not to lose whether includes Dress/Pant/Skirt/etc
dataset['Pant'] = dataset.groupby(['Img', 'Date'])['Pant'].transform('sum').clip_upper(1.0)
dataset['Skirt'] = dataset.groupby(['Img', 'Date'])['Skirt'].transform('sum').clip_upper(1.0)
dataset['Dress'] = dataset.groupby(['Img', 'Date'])['Dress'].transform('sum').clip_upper(1.0)
dataset['Shirt'] = dataset.groupby(['Img', 'Date'])['Shirt'].transform('sum').clip_upper(1.0)
dataset = dataset.drop_duplicates(subset=['Img', 'Date'])

print(dataset.shape)
#print(clusters.shape)
#print(headers.shape)
print(dataset.nunique())

dataset = dataset.sample(frac=1).reset_index(drop=True)

#Order the cluster set the same order as the dataset alphabetically.
data = np.empty((dataset.shape[0], 512, 341))
for index, row in dataset.iterrows():
   data[index] = clustered[row['File']]
clustered.close()

print(data[0].shape)
#data is X, dataset['Shirt', 'Pant', 'Skirt', 'Dress'] is y
#Only import keras if everything else works, since keras requires GPU and takes time to initialize

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Conv3D, MaxPooling3D
from keras import backend as K

data /= 4

if K.image_data_format() == 'channels_first':
   print("ERROR: Reshape NumPy array!")

data = data.reshape((data.shape[0], data.shape[1], data.shape[2], 1))

x_train = data[:886]
x_test = data[886:]
y = dataset[['Shirt', 'Skirt', 'Pant', 'Dress']].values
y_train = y[:886]
y_test = y[886:]

#Use ImageDatasetGenerator to maybe vastly increase size of dataset!
batch_size = 8
epochs = 12

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(512, 341, 1)))
#model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4, activation='softmax')) #Number of classes is 4

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
