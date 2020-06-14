import cv2
from os import path
import numpy as np
from time import time
import matplotlib.pyplot as plt

def ex1():
    for i in range(1, 12):
        x_img = cv2.imread("../bola/bola_" + str(i) +".tiff", cv2.IMREAD_GRAYSCALE)
        cv2.imwrite("bola_" + str(i) + ".jpeg", x_img, (cv2.IMWRITE_JPEG_QUALITY, 50))

ex1()