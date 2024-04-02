import cv2
import sys
from matplotlib import pyplot as plt

imagePath = r'image0.jpg'
dirCascadeFiles = r'../opencv/haarcascades_cuda/'
cascadefile = dirCascadeFiles + "haarcascade_frontalface_default.xml"
classCascade = cv2.CascadeClassifier(cascadefile)
image = cv2.imread(imagePath)
plt.imshow(image)