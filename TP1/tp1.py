import cv2
import numpy as np
import matplotlib.pyplot as plt

def ex1():
    x_img = cv2.imread("lenac.tif")
    cv2.imshow('OriginalImg', x_img)
    print(x_img.dtype)
    print(x_img.shape)

    cv2.imwrite('file1.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 80))
    cv2.imwrite('file2.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 10))


    y_img = cv2.imread("file1.jpg")
    z_img = cv2.imread("file2.jpg")

    cv2.imshow('Original Image', x_img)
    cv2.imshow('80% Image', y_img)
    cv2.imshow('10% Image', z_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    x_img_g = cv2.cvtColor(x_img , cv2.COLOR_BGR2GRAY)
    cv2.imshow (' Gray Image ' , x_img_g )
    cv2.imwrite(' file3.bmp' , x_img_g )

if __name__ == '__main__':
    ex1()
    print('fim')