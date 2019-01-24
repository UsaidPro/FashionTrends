"""
Preprocesses images to reduce noise and generate dataset for training
"""
import cv2
import glob
from model import Deeplabv3
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from pprint import pprint

image_dir = 'C:/Users/usaid/Desktop/FashionTrends/Image_Data/Chictopia/Parsed/'
images = glob.glob(image_dir + '*.jpg')

#Initialize DeepLab model
deeplab_model = Deeplabv3()
#I picked 4 because I felt that it works. Should test out more variations to see if accuracy improves
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
   
      #Applying mask to convert non-human elements to black background
      masked_image = cv2.bitwise_and(resized_original, resized_original, mask=labels[:512 - pad_x, :512 - pad_y].astype(np.uint8))
      #Locate human elements (not-black)
      ret, thresh = cv2.threshold(cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY), 5, 255, cv2.THRESH_BINARY)
      image, contours, hireachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
      #Create smallest bounding box that contains all elements
      lx = 100000000
      ly = 100000000
      rx = 0
      ry = 0
      for contour in contours:
         largest = max(contours, key=cv2.contourArea)
         x, y, w, h = cv2.boundingRect(largest)
         lx = min(x, lx)
         ly = min(y, ly)
         rx = max(x+w, rx)
         ry = max(y+h, ry)
      #No need to check if contours don't exist due to checking if 15 is in labels before
      crop = masked_image[ly:ry, lx:rx]
      """
      #Make image even for quicker resizing - commenting this all out since it will only speedup since cv2.pyrDown
      #and pyrDown() only downscales by factors of 2.
      if crop.shape[0] % 2 != 0:
         crop = np.vstack((crop, np.zeros((1, crop.shape[1], 3))))
      if crop.shape[1] % 2 != 0:
         crop = np.hstack((crop, np.zeros((crop.shape[0], 1, 3))))
      """
      print(crop.shape)
      #Converting image shape to square
      if crop.shape[0] > crop.shape[1]:
         crop = np.hstack((np.zeros((crop.shape[0], int((crop.shape[0] - crop.shape[1]) / 2), 3)), crop, np.zeros((crop.shape[0], int((crop.shape[0] - crop.shape[1]) / 2), 3))))
      elif crop.shape[0] < crop.shape[1]:
         crop = np.vstack((np.zeros((int((crop.shape[1] - crop.shape[0]) / 2), crop.shape[1], 3)), crop, np.zeros((int((crop.shape[1] - crop.shape[0]) / 2), crop.shape[1], 3))))
      #Resizing image
      resized_image = cv2.resize(crop, (128, 128))

      w, h, d = resized_image.shape
      flat_image = np.reshape(resized_image, (w * h, d))
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
      
      cv2.imwrite(image_dir + "Clustered/" + os.path.basename(img), final)
      #I also save a Numpy array of the clusters (a 2D array of cluster labels) for training to test 
      #whether training just based on clusters rather than colors affects accuracy of model
      np.save(image_dir + "Clustered/" + os.path.basename(img).replace('.jpg', '.npy'), final_flat)
   else:
      cv2.imwrite(image_dir + "NotHuman/" + os.path.basename(img), image)
   i += 1