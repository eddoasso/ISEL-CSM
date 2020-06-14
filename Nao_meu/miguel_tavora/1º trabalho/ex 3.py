import cv2
import numpy as np
import matplotlib.pyplot as plt

x_img = cv2.imread( "lenac.tif" )

x_img_g = cv2.cvtColor(x_img , cv2 .COLOR_BGR2GRAY)
cv2.imshow('Gray Image' , x_img_g)
cv2.imwrite('file3.bmp' , x_img_g)

plt.plot('m')
plt.hist(x_img_g.ravel( ),256,[0,256])
plt.show();

cv2.waitKey ( 0 )
cv2.destroyAllWindows ( )

