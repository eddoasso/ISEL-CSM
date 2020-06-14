import cv2
import numpy as np
import matplotlib.pyplot as plt

x_img = cv2.imread( "lenac.tif" )

x_img_g = cv2.cvtColor(x_img , cv2 .COLOR_BGR2GRAY)
cv2.imshow('Gray Image' , x_img_g)
cv2.imwrite('file3.bmp' , x_img_g)

y = x_img_g > 128
cv2.imshow('BW',y*255)

cv2.waitKey ( 0 )
cv2.destroyAllWindows ( )

