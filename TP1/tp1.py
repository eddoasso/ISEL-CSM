import cv2
import numpy as np
import matplotlib.pyplot as plt


def ex1():
    x_img = cv2.imread("lenac.tif")
    print(x_img.dtype)
    print(x_img.shape)

    cv2.imwrite('file1.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 80))
    cv2.imwrite('file2.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 10))

    img_80 = cv2.imread("file1.jpg")
    img_10 = cv2.imread("file2.jpg")

    cv2.imshow('Original Image', x_img)
    cv2.imshow('80 img', img_80)
    cv2.imshow('10 img', img_10)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    ex1()
    print('fim')
