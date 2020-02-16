import numpy as np
import cv2

# load image
img = cv2.imread('Capture.JPG')

#convert to gray
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# use thrashold
ret, thresh = cv2.threshold(img_gray, 127, 255, 0)

image, contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# draw contours
img = cv2.drawContours(image, contours, -1, (0,255,0), 3)

cv2.waitKey(0)
#cv2.destoryAllWindows()

print("didn't do shittt")
