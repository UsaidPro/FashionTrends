import cv2
import glob
from model import Deeplabv3
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from pprint import pprint

images = glob.glob("C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/*.jpg")

deeplab_model = Deeplabv3()
kmeans = KMeans(4)
print("Initialized Pipeline")
i = 0
for img in images:
   image = plt.imread(img)
   w, h, _ = image.shape
   ratio = 512. / np.max([w,h])
   resized_original = cv2.resize(image,(int(ratio*h),int(ratio*w)))
   resized = resized_original / 127.5 - 1.
   pad_x = int(512 - resized.shape[0])
   pad_y = int(512 - resized.shape[1])
   resized2 = np.pad(resized,((0,pad_x),(0,pad_y),(0,0)),mode='constant')
   res = deeplab_model.predict(np.expand_dims(resized2,0))
   labels = np.argmax(res.squeeze(),-1)
   print(labels[:512 - pad_x, :512 - pad_y].shape)
   np.place(labels, labels != 15, [0])
   if(15 in labels):
      np.place(labels, labels == 15, [255])
      #r, g, b = cv2.split(resized_original)
      #masked_image = cv2.merge((r, g, b, labels[:512 - pad_x, :512 - pad_y].astype(np.uint8)))
   
      #masked_image[masked_image[:, :, 3] == 255] = 0
   
      #Uncomment for black background
      masked_image = cv2.bitwise_and(resized_original, resized_original, mask=labels[:512 - pad_x, :512 - pad_y].astype(np.uint8))
      
      #Clustering
      w, h, d = masked_image.shape
      flat_image = np.reshape(masked_image, (w * h, d))
      labels = kmeans.fit_predict(flat_image)
      labels_reshaped = labels.reshape((w, h, 1))
      final = np.zeros((w, h, d))
      final_flat = np.zeros((w, h))
      order = np.column_stack(np.unique(labels, return_counts=True)) #Returns (array([0, 1, 2, 3]), array([219401,   8962,  20655,  13126], dtype=int64))
      order = order[order[:, 1].argsort()[::-1]]
      #Find index of ix in order and 
      for ix in range(len(kmeans.cluster_centers_)):
         final[labels_reshaped[:, :, 0] == ix] = kmeans.cluster_centers_[ix]
         i = np.where(order[:, 0] == ix)[0][0]
         final_flat[labels_reshaped[:, :, 0] == ix] = i
      
      #cv2.cvtColor(final, cv2.COLOR_RGBA2BGRA, final)
      #cv2.imwrite("C:/Users/usaid/Desktop/FashionTrends/AliImages/Cluster/" + os.path.basename(img).replace('jpg', 'png'), final)
      cv2.imwrite("C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/Clustered/" + os.path.basename(img), final)
      np.save("C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/Clustered/" + os.path.basename(img).replace('.jpg', '.npy'), final_flat)
   else:
      cv2.imwrite("C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/NotHuman/" + os.path.basename(img), image)
   i += 1